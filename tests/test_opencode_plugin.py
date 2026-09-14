import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which("node"), "node is required for the OpenCode plugin")
class OpenCodePluginTest(unittest.TestCase):
    """Mirror tests/test_always_on_hooks.py for the OpenCode server plugin: the
    always-on flag gates injection, and frontmatter stripping matches the hooks."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        # Resolve the temp root: on macOS /var is a symlink to /private/var, so
        # the path Python's tempfile reports (/var/...) differs from the
        # realpath the Node plugin resolves to (/private/var/...). Matching the
        # two keeps the skill-path assertions stable across platforms.
        temp_root = Path(os.path.realpath(self.temp_dir.name))
        self.plugin_root = temp_root / "plugin"
        shutil.copytree(ROOT / ".opencode", self.plugin_root / ".opencode")
        shutil.copytree(ROOT / "skills", self.plugin_root / "skills")
        # The plugin reads its flag from $XDG_CONFIG_HOME/opencode/.i-have-adhd-always.
        self.config_dir = temp_root / "config"
        (self.config_dir / "opencode").mkdir(parents=True)

    def run_plugin(self, mode=None, config=None):
        env = os.environ.copy()
        env["XDG_CONFIG_HOME"] = str(self.config_dir)
        args = [
            "node",
            str(ROOT / "tests" / "opencode_plugin_driver.mjs"),
            str(self.plugin_root / ".opencode" / "plugins" / "i-have-adhd.mjs"),
        ]
        if mode:
            args.append(mode)
        if config is not None:
            args.append(json.dumps(config))
        return subprocess.run(
            args,
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )

    def opt_in(self):
        (self.config_dir / "opencode" / ".i-have-adhd-always").touch()

    def write_skill(self, text):
        (self.plugin_root / "skills" / "i-have-adhd" / "SKILL.md").write_text(text)

    def test_silent_without_opt_in_flag(self):
        result = self.run_plugin()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("", result.stdout)

    def test_strips_frontmatter_with_trailing_whitespace(self):
        self.write_skill("---   \nname: fixture\n--- \t\nFixture body.\n")
        self.opt_in()
        result = self.run_plugin()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertNotIn("name: fixture", result.stdout)
        self.assertIn("\n\nFixture body.", result.stdout)

    def test_keeps_content_when_frontmatter_is_unclosed(self):
        self.write_skill("---\nname: fixture\nFixture body, fence never closed.\n")
        self.opt_in()
        result = self.run_plugin()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("Fixture body, fence never closed.", result.stdout)

    def test_config_hook_registers_the_slash_command(self):
        # Regression test for #140: a global install (plugin loaded from a
        # path outside any checkout, no project-scope .opencode/command/
        # directory in play) must still get /i-have-adhd, because OpenCode's
        # skill-sourced commands are not surfaced in the TUI's `/` menu.
        result = self.run_plugin(mode="config")
        self.assertEqual(0, result.returncode, result.stderr)
        config = json.loads(result.stdout)
        command = config["command"]["i-have-adhd"]
        self.assertIn("ADHD", command["description"])
        self.assertIn("stop adhd mode", command["template"])

    def test_config_hook_still_registers_the_skills_path(self):
        result = self.run_plugin(mode="config")
        self.assertEqual(0, result.returncode, result.stderr)
        config = json.loads(result.stdout)
        self.assertIn(str(self.plugin_root / "skills"), config["skills"]["paths"])

    def test_config_preserves_existing_command(self):
        custom = {"description": "User command", "template": "Keep this", "agent": "plan"}
        result = self.run_plugin("config", {"command": {"i-have-adhd": custom}})
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(custom, json.loads(result.stdout)["command"]["i-have-adhd"])

    def test_repeated_config_does_not_duplicate_skill_paths(self):
        result = self.run_plugin("config")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual([str(self.plugin_root / "skills")], json.loads(result.stdout)["skills"]["paths"])

    def test_command_preserves_metadata_and_trims_template(self):
        metadata = {"description": 'ADHD: "focus"\nnext line', "agent": "plan",
                    "model": "fixture/model", "subtask": True}
        command = self.plugin_root / ".opencode/command/i-have-adhd.md"
        command.write_bytes(("---  \r\n" + json.dumps(metadata) +
                             "\r\n--- \t\r\n\r\nUse the skill.\r\n\r\n").encode())
        result = self.run_plugin("config")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual({**metadata, "template": "Use the skill."},
                         json.loads(result.stdout)["command"]["i-have-adhd"])

    def test_missing_command_keeps_skill_discovery(self):
        (self.plugin_root / ".opencode/command/i-have-adhd.md").unlink()
        result = self.run_plugin("config")
        self.assertEqual(0, result.returncode, result.stderr)
        config = json.loads(result.stdout)
        self.assertNotIn("i-have-adhd", config["command"])
        self.assertEqual([str(self.plugin_root / "skills")], config["skills"]["paths"])

    def test_malformed_command_does_not_leak_frontmatter_into_prompt(self):
        command = self.plugin_root / ".opencode/command/i-have-adhd.md"
        for text in ["---\n{broken}\n---\nBody", '---\n{"description":"unclosed"}\nBody']:
            with self.subTest(text=text):
                command.write_text(text)
                result = self.run_plugin("config")
                self.assertEqual(0, result.returncode, result.stderr)
                config = json.loads(result.stdout)
                self.assertNotIn("i-have-adhd", config["command"])
                self.assertEqual([str(self.plugin_root / "skills")], config["skills"]["paths"])


if __name__ == "__main__":
    unittest.main()
