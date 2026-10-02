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

    def run_launcher(self, command, env):
        # Run a hooks.json command the way Claude Code actually runs a
        # shell-form hook: `sh -c` on macOS/Linux, Git Bash on Windows.
        # subprocess.run(shell=True) resolves to cmd.exe on Windows, which is
        # a shell Claude Code never selects, so a POSIX launcher would be
        # asserted against the wrong interpreter and fail for a reason no user
        # would ever hit. Prefer a real POSIX shell and skip rather than
        # pretend cmd.exe is a supported runtime.
        payload = json.dumps(
            {
                "session_id": "test-session",
                "cwd": str(self.plugin_root),
                "hook_event_name": "SessionStart",
                "source": "startup",
            }
        )
        kwargs = dict(
            check=False,
            capture_output=True,
            env=env,
            input=payload,
            text=True,
        )
        if sh := shutil.which("sh"):
            return subprocess.run([sh, "-c", command], **kwargs)
        return subprocess.run(command, shell=True, **kwargs)

    def run_codex_hook(self, plugin_root=None, root_vars=None):
        config = json.loads((ROOT / "hooks" / "hooks.json").read_text())
        hook = config["hooks"]["SessionStart"][0]["hooks"][0]
        env = os.environ.copy()
        env["CLAUDE_CONFIG_DIR"] = str(self.config_dir)
        plugin_root = plugin_root or self.plugin_root
        if root_vars is None:
            env["CLAUDE_PLUGIN_ROOT"] = str(plugin_root)
            env["PLUGIN_ROOT"] = str(plugin_root)
        else:
            # root_vars names the variables the runtime is assumed to export,
            # so a launcher that reads only one of them can be caught.
            for name, value in root_vars.items():
                env[name] = str(value)
        return self.run_launcher(hook["command"], env)

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

    def test_launcher_honours_the_codex_plugin_root_variable(self):
        # The Codex CLI exports PLUGIN_ROOT and does not set
        # CLAUDE_PLUGIN_ROOT. Proving the launcher reads PLUGIN_ROOT through
        # behaviour, rather than by matching the command text, keeps this test
        # meaningful if the launcher is ever rewritten.
        if not shutil.which("sh"):
            self.skipTest("no POSIX shell available to run the launcher")

        (self.config_dir / ".i-have-adhd-always").touch()
        result = self.run_codex_hook(root_vars={"PLUGIN_ROOT": self.plugin_root})

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("ADHD MODE ACTIVE (always-on)", result.stdout)

    def test_launcher_honours_the_claude_plugin_root_variable(self):
        if not shutil.which("sh"):
            self.skipTest("no POSIX shell available to run the launcher")

        (self.config_dir / ".i-have-adhd-always").touch()
        result = self.run_codex_hook(root_vars={"CLAUDE_PLUGIN_ROOT": self.plugin_root})

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("ADHD MODE ACTIVE (always-on)", result.stdout)

    def test_hook_uses_a_shared_claude_and_codex_launcher(self):
        config = json.loads((ROOT / "hooks" / "hooks.json").read_text())
        hook = config["hooks"]["SessionStart"][0]["hooks"][0]

        self.assertNotIn("args", hook)
        command = hook["command"]

        # The launcher must stay runnable on machines where Node is absent,
        # which is the whole point of this hook (issue #221).
        self.assertNotIn("node", command)

        # It must invoke the POSIX hook script and never block session start.
        self.assertIn("always-on.sh", command)
        self.assertIn("exit 0", command)


if __name__ == "__main__":
    unittest.main()
