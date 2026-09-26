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
    always-on flag gates injection, and frontmatter stripping matches the hooks.

    OpenCode V2 replaced the V1 `config` mutation hook with `ctx.skill.transform`
    and `ctx.command.transform`, so registration is asserted through those."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.plugin_root = Path(self.temp_dir.name) / "plugin"
        shutil.copytree(ROOT / ".opencode", self.plugin_root / ".opencode")
        shutil.copytree(ROOT / "skills", self.plugin_root / "skills")
        # The plugin reads its flag from $XDG_CONFIG_HOME/opencode/.i-have-adhd-always.
        self.config_dir = Path(self.temp_dir.name) / "config"
        (self.config_dir / "opencode").mkdir(parents=True)

    def run_plugin(self, mode=None):
        env = os.environ.copy()
        env["XDG_CONFIG_HOME"] = str(self.config_dir)
        args = [
            "node",
            str(ROOT / "tests" / "opencode_plugin_driver.mjs"),
            str(self.plugin_root / ".opencode" / "plugins" / "i-have-adhd.mjs"),
        ]
        if mode:
            args.append(mode)
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

    def test_setup_registers_the_slash_command(self):
        # Regression test for #140: a global install (plugin loaded from a
        # path outside any checkout, no project-scope .opencode/command/
        # directory in play) must still get /i-have-adhd, because OpenCode's
        # skill-sourced commands are not surfaced in the TUI's `/` menu.
        result = self.run_plugin(mode="command")
        self.assertEqual(0, result.returncode, result.stderr)
        command = json.loads(result.stdout)[0]
        self.assertEqual("i-have-adhd", command["name"])
        self.assertIn("ADHD", command["description"])
        self.assertIn("stop adhd mode", command["template"])

    def test_setup_registers_the_skill(self):
        result = self.run_plugin(mode="skill")
        self.assertEqual(0, result.returncode, result.stderr)
        skill = json.loads(result.stdout)[0]
        self.assertEqual("i-have-adhd", skill["id"])
        self.assertEqual(
            str(self.plugin_root / "skills" / "i-have-adhd" / "SKILL.md"), skill["path"]
        )
        self.assertIn("ADHD", skill["description"])
        self.assertNotIn("---", skill["content"])

    def test_missing_command_keeps_skill_registration(self):
        (self.plugin_root / ".opencode/command/i-have-adhd.md").unlink()
        result = self.run_plugin(mode="command")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual([], json.loads(result.stdout))
        result = self.run_plugin(mode="skill")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("i-have-adhd", json.loads(result.stdout)[0]["id"])

    def test_malformed_command_keeps_skill_registration(self):
        command = self.plugin_root / ".opencode/command/i-have-adhd.md"
        for text in ["---\n{broken}\n---\nBody", '---\n{"description":"unclosed"}\nBody']:
            with self.subTest(text=text):
                command.write_text(text)
                result = self.run_plugin(mode="command")
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual([], json.loads(result.stdout))
                result = self.run_plugin(mode="skill")
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual("i-have-adhd", json.loads(result.stdout)[0]["id"])


if __name__ == "__main__":
    unittest.main()
