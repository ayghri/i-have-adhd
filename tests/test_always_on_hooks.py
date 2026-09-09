import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AlwaysOnHookTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.plugin_root = Path(self.temp_dir.name) / "plugin with spaces"
        shutil.copytree(ROOT / "hooks", self.plugin_root / "hooks")
        shutil.copytree(ROOT / "skills", self.plugin_root / "skills")
        self.config_dir = Path(self.temp_dir.name) / "claude config"
        self.config_dir.mkdir()

    def runtimes(self):
        runtimes = []
        if node := shutil.which("node"):
            runtimes.append(("node", [node, self.plugin_root / "hooks" / "always-on.mjs"]))
        if sh := shutil.which("sh"):
            runtimes.append(("sh", [sh, self.plugin_root / "hooks" / "always-on.sh"]))
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
                )
            )
        return runtimes

    def run_hook(self, command):
        env = os.environ.copy()
        env["CLAUDE_CONFIG_DIR"] = str(self.config_dir)
        return subprocess.run(
            [str(part) for part in command],
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )

    def run_codex_hook(self, plugin_root=None):
        config = json.loads((ROOT / "hooks" / "hooks.json").read_text())
        hook = config["hooks"]["SessionStart"][0]["hooks"][0]
        env = os.environ.copy()
        env["CLAUDE_CONFIG_DIR"] = str(self.config_dir)
        plugin_root = plugin_root or self.plugin_root
        env["CLAUDE_PLUGIN_ROOT"] = str(plugin_root)
        env["PLUGIN_ROOT"] = str(plugin_root)
        return subprocess.run(
            hook["command"],
            check=False,
            capture_output=True,
            env=env,
            input=json.dumps(
                {
                    "session_id": "test-session",
                    "cwd": str(self.plugin_root),
                    "hook_event_name": "SessionStart",
                    "source": "startup",
                }
            ),
            shell=True,
            text=True,
        )

    @staticmethod
    def normalize(stdout):
        # The banner embeds the flag path. On Windows the sh runtime joins it
        # with "/" while node and PowerShell join with "\"; both name the same
        # file, so unify separators (and newlines) before comparing runtimes.
        return stdout.replace("\r\n", "\n").replace("\\", "/")

    def test_hook_is_silent_without_opt_in_flag(self):
        self.assertTrue(self.runtimes(), "no hook runtime is available")

        for name, command in self.runtimes():
            with self.subTest(runtime=name):
                result = self.run_hook(command)
                self.assertEqual(0, result.returncode)
                self.assertEqual("", result.stdout)
                self.assertEqual("", result.stderr)

    def test_runtimes_strip_frontmatter_with_trailing_whitespace(self):
        skill_path = self.plugin_root / "skills" / "i-have-adhd" / "SKILL.md"
        skill_path.write_text("---   \nname: fixture\n--- \t\nFixture body.\n")
        (self.config_dir / ".i-have-adhd-always").touch()
        outputs = {}

        for name, command in self.runtimes():
            with self.subTest(runtime=name):
                result = self.run_hook(command)
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
        (self.config_dir / ".i-have-adhd-always").touch()
        outputs = {}

        for name, command in self.runtimes():
            with self.subTest(runtime=name):
                result = self.run_hook(command)
                self.assertEqual(0, result.returncode)
                self.assertEqual("", result.stderr)
                normalized = self.normalize(result.stdout)
                self.assertIn("Fixture body, fence never closed.", normalized)
                outputs[name] = normalized

        self.assertEqual(1, len(set(outputs.values())))

    def test_codex_command_runs_the_hook_instead_of_parsing_session_json(self):
        (self.config_dir / ".i-have-adhd-always").touch()

        result = self.run_codex_hook()

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("", result.stderr)
        self.assertIn("ADHD MODE ACTIVE (always-on)", result.stdout)

    def test_codex_command_is_silent_without_opt_in_flag(self):
        result = self.run_codex_hook()

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("", result.stderr)
        self.assertEqual("", result.stdout)

    def test_codex_command_swallows_missing_plugin_errors(self):
        result = self.run_codex_hook(self.plugin_root / "missing plugin")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("", result.stderr)
        self.assertEqual("", result.stdout)

    def test_hook_uses_a_shared_claude_and_codex_launcher(self):
        config = json.loads((ROOT / "hooks" / "hooks.json").read_text())
        hook = config["hooks"]["SessionStart"][0]["hooks"][0]

        self.assertNotIn("args", hook)
        command = hook["command"]
        self.assertRegex(command, r'^node(?: --input-type=module)? -e "')
        self.assertIn("process.env.CLAUDE_PLUGIN_ROOT", command)
        self.assertIn("process.env.PLUGIN_ROOT", command)
        self.assertIn("await import", command)
        self.assertIn(".catch", command)


if __name__ == "__main__":
    unittest.main()
