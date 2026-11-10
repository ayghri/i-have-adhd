import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTICE = (
    "i-have-adhd: couldn't tell if a human is reading; rules not loaded. "
    "Run /i-have-adhd to turn them on."
)


class AlwaysOnHookTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.plugin_root = Path(self.temp_dir.name) / "plugin with spaces"
        shutil.copytree(ROOT / "hooks", self.plugin_root / "hooks")
        shutil.copytree(ROOT / "skills", self.plugin_root / "skills")
        self.config_dir = Path(self.temp_dir.name) / "claude config"
        self.config_dir.mkdir()
        self.home_dir = Path(self.temp_dir.name) / "home"
        self.home_dir.mkdir()
        self.log = self.home_dir / ".local" / "state" / "i-have-adhd" / "decisions.log"

    def runtimes(self):
        # The Node path is the one that gates on session kind, so only that path
        # gets the human signal; the native fallbacks must render the same text.
        runtimes = []
        if node := shutil.which("node"):
            runtimes.append(
                (
                    "node",
                    [node, self.plugin_root / "hooks" / "always-on.mjs", "--agent", "claude"],
                    {"CLAUDE_CODE_SESSION_ATTENDED": "1"},
                )
            )
        if sh := shutil.which("sh"):
            runtimes.append(
                ("sh", [sh, self.plugin_root / "hooks" / "always-on.sh"], {})
            )
        if powershell := shutil.which("pwsh") or shutil.which("powershell"):
            runtimes.append(
                (
                    "powershell",
                    [
                        powershell,
                        "-NoProfile",
                        "-ExecutionPolicy",
                        "Bypass",
                        "-File",
                        self.plugin_root / "hooks" / "always-on.ps1",
                    ],
                    {},
                )
            )
        return runtimes

    def env(self, **overrides):
        env = os.environ.copy()
        for key in ("I_HAVE_ADHD", "I_HAVE_ADHD_LOG", "CLAUDE_CODE_SESSION_ATTENDED"):
            env.pop(key, None)
        env.update(
            {
                "HOME": str(self.home_dir),
                "USERPROFILE": str(self.home_dir),
                "CLAUDE_CONFIG_DIR": str(self.config_dir),
                "CLAUDE_PLUGIN_ROOT": str(self.plugin_root),
                "PLUGIN_ROOT": str(self.plugin_root),
            }
        )
        env.update(overrides)
        return env

    def run_hook(self, command, extra_env=None):
        return subprocess.run(
            [str(part) for part in command],
            check=False,
            capture_output=True,
            text=True,
            env=self.env(**(extra_env or {})),
        )

    def run_node_hook(self, **overrides):
        return self.run_hook(self.runtimes()[0][1], overrides)

    def run_plugin_hook(self, **overrides):
        config = json.loads((ROOT / "hooks" / "hooks.json").read_text())
        hook = config["hooks"]["SessionStart"][0]["hooks"][0]
        return subprocess.run(
            hook["command"],
            check=False,
            capture_output=True,
            env=self.env(**overrides),
            input=json.dumps(
                {
                    "session_id": "test-session",
                    "cwd": str(self.plugin_root),
                    "hook_event_name": "SessionStart",
                    "source": "startup",
                }
            ).encode("utf8"),
            shell=True,
        )

    @staticmethod
    def normalize(stdout):
        # The banner embeds the flag path. On Windows the sh runtime joins it
        # with "/" while node and PowerShell join with "\"; both name the same
        # file, so unify separators (and newlines) before comparing runtimes.
        return stdout.replace("\r\n", "\n").replace("\\", "/")

    def opt_in(self, contents=""):
        (self.config_dir / ".i-have-adhd-always").write_text(contents)

    def test_hook_is_silent_without_opt_in_flag(self):
        self.assertTrue(self.runtimes(), "no hook runtime is available")

        for name, command, extra_env in self.runtimes():
            with self.subTest(runtime=name):
                result = self.run_hook(command, extra_env)
                self.assertEqual(0, result.returncode)
                self.assertEqual("", result.stdout)
                self.assertEqual("", result.stderr)
        self.assertFalse(self.log.exists())
        self.assertFalse((self.home_dir / ".local" / "state" / "i-have-adhd").exists())

    def test_claude_human_injects_and_nonhuman_is_silent(self):
        self.opt_in()

        human = self.run_node_hook(CLAUDE_CODE_SESSION_ATTENDED="1")
        self.assertEqual(0, human.returncode, human.stderr)
        self.assertIn("ADHD MODE ACTIVE (always-on)", human.stdout)
        self.assertIn("Working memory is small", human.stdout)

        nonhuman = self.run_node_hook(CLAUDE_CODE_SESSION_ATTENDED="0")
        self.assertEqual(0, nonhuman.returncode, nonhuman.stderr)
        self.assertEqual("", nonhuman.stdout)

    def test_claude_unclear_returns_only_system_message(self):
        self.opt_in()

        result = self.run_node_hook()

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertRegex(result.stdout, r"^\{.*\}$")
        payload = json.loads(result.stdout)
        self.assertEqual({"systemMessage": NOTICE}, payload)

    def test_claude_opt_out_wins(self):
        self.opt_in()

        result = self.run_node_hook(
            CLAUDE_CODE_SESSION_ATTENDED="1", I_HAVE_ADHD="0"
        )

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("", result.stdout)

    def test_runtimes_strip_frontmatter_with_trailing_whitespace(self):
        skill_path = self.plugin_root / "skills" / "i-have-adhd" / "SKILL.md"
        skill_path.write_text("---   \nname: fixture\n--- \t\nFixture body.\n")
        self.opt_in()
        outputs = {}

        for name, command, extra_env in self.runtimes():
            with self.subTest(runtime=name):
                result = self.run_hook(command, extra_env)
                self.assertEqual(0, result.returncode)
                self.assertEqual("", result.stderr)
                normalized = self.normalize(result.stdout)
                self.assertNotIn("name: fixture", normalized)
                self.assertIn("\n\nFixture body.\n", normalized)
                outputs[name] = normalized

        self.assertEqual(1, len(set(outputs.values())))

    def test_runtimes_keep_content_when_frontmatter_is_unclosed(self):
        # An opening --- with no closing delimiter is not frontmatter. Keeping
        # the whole file beats injecting a banner that promises "the ruleset
        # below" followed by nothing.
        skill_path = self.plugin_root / "skills" / "i-have-adhd" / "SKILL.md"
        skill_path.write_text("---\nname: fixture\nFixture body, fence never closed.\n")
        self.opt_in()
        outputs = {}

        for name, command, extra_env in self.runtimes():
            with self.subTest(runtime=name):
                result = self.run_hook(command, extra_env)
                self.assertEqual(0, result.returncode)
                self.assertEqual("", result.stderr)
                normalized = self.normalize(result.stdout)
                self.assertIn("Fixture body, fence never closed.", normalized)
                outputs[name] = normalized

        self.assertEqual(1, len(set(outputs.values())))

    def test_launcher_runs_the_hook_instead_of_parsing_session_json(self):
        self.opt_in()

        result = self.run_plugin_hook(CLAUDE_CODE_SESSION_ATTENDED="1")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(b"", result.stderr)
        self.assertIn(b"ADHD MODE ACTIVE (always-on)", result.stdout)

    def test_launcher_is_silent_without_opt_in_flag(self):
        result = self.run_plugin_hook(CLAUDE_CODE_SESSION_ATTENDED="1")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(b"", result.stderr)
        self.assertEqual(b"", result.stdout)

    def test_launcher_swallows_missing_plugin_errors(self):
        result = self.run_plugin_hook(
            CLAUDE_CODE_SESSION_ATTENDED="1",
            CLAUDE_PLUGIN_ROOT=str(self.plugin_root / "missing plugin"),
            PLUGIN_ROOT=str(self.plugin_root / "missing plugin"),
        )

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(b"", result.stderr)
        self.assertEqual(b"", result.stdout)

    def test_shipped_launchers_select_their_runtime(self):
        self.assertTrue((ROOT / "hooks" / "hooks.codex.json").is_file())
        claude = json.loads((ROOT / "hooks" / "hooks.json").read_text())
        codex = json.loads((ROOT / "hooks" / "hooks.codex.json").read_text())
        claude_hook = claude["hooks"]["SessionStart"][0]["hooks"][0]
        codex_hook = codex["hooks"]["SessionStart"][0]["hooks"][0]

        for hook in (claude_hook, codex_hook):
            self.assertNotIn("args", hook)
            command = hook["command"]
            self.assertRegex(command, r'^node(?: --input-type=module)? -e "')
            self.assertIn("process.env.CLAUDE_PLUGIN_ROOT", command)
            self.assertIn("process.env.PLUGIN_ROOT", command)
            self.assertIn("await import", command)
            self.assertIn(".catch", command)

        self.assertTrue(claude_hook["command"].rstrip().endswith("--agent claude"))
        self.assertIn("--agent codex --json", codex_hook["command"])

    def test_codex_manifest_uses_the_codex_hook_file(self):
        path = ROOT / ".codex-plugin" / "plugin.json"
        manifest = json.loads(path.read_text())

        self.assertIn("hooks", manifest)
        self.assertEqual("./hooks/hooks.codex.json", manifest["hooks"])
        self.assertTrue((ROOT / manifest["hooks"]).is_file())


if __name__ == "__main__":
    unittest.main()
