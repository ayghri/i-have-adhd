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
        self.plugin_root = Path(self.temp_dir.name) / "plugin"
        shutil.copytree(ROOT / ".opencode", self.plugin_root / ".opencode")
        shutil.copytree(ROOT / "skills", self.plugin_root / "skills")
        # The plugin reads its flag from $XDG_CONFIG_HOME/opencode/.i-have-adhd-always.
        self.config_dir = Path(self.temp_dir.name) / "config"
        (self.config_dir / "opencode").mkdir(parents=True)

    def run_plugin(self):
        env = os.environ.copy()
        env["XDG_CONFIG_HOME"] = str(self.config_dir)
        return subprocess.run(
            [
                "node",
                str(ROOT / "tests" / "opencode_plugin_driver.mjs"),
                str(self.plugin_root / ".opencode" / "plugins" / "i-have-adhd.mjs"),
            ],
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )

    def run_config_hook(self, config=None):
        env = os.environ.copy()
        env["XDG_CONFIG_HOME"] = str(self.config_dir)
        return subprocess.run(
            [
                "node",
                str(ROOT / "tests" / "opencode_plugin_config_driver.mjs"),
                str(self.plugin_root / ".opencode" / "plugins" / "i-have-adhd.mjs"),
                json.dumps(config if config is not None else {}),
            ],
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )

    def command_markdown(self):
        text = (
            self.plugin_root / ".opencode" / "command" / "i-have-adhd.md"
        ).read_text(encoding="utf-8")
        fence = "---"
        if not text.startswith(fence):
            return "", text.strip()
        rest = text[len(fence) :].lstrip("\r\n")
        fm, _, body = rest.partition("\n" + fence)
        description = ""
        for line in fm.splitlines():
            if line.startswith("description:"):
                description = line.split(":", 1)[1].strip()
                break
        return description, body.strip()

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

    def test_config_hook_registers_slash_command(self):
        result = self.run_config_hook({})
        self.assertEqual(0, result.returncode, result.stderr)
        config = json.loads(result.stdout)
        description, template = self.command_markdown()
        command = config.get("command", {}).get("i-have-adhd")
        self.assertIsNotNone(command)
        self.assertEqual(description, command["description"])
        # Node fs.readFileSync keeps CRLF; Path.read_text uses universal newlines.
        self.assertEqual(template, command["template"].replace("\r\n", "\n"))

    def test_config_hook_keeps_existing_commands(self):
        result = self.run_config_hook(
            {"command": {"other": {"template": "keep me"}}}
        )
        self.assertEqual(0, result.returncode, result.stderr)
        config = json.loads(result.stdout)
        self.assertEqual("keep me", config["command"]["other"]["template"])
        self.assertIn("i-have-adhd", config["command"])

    def test_config_hook_tolerates_missing_command_file(self):
        (self.plugin_root / ".opencode" / "command" / "i-have-adhd.md").unlink()
        result = self.run_config_hook({})
        self.assertEqual(0, result.returncode, result.stderr)
        config = json.loads(result.stdout)
        self.assertNotIn("i-have-adhd", config.get("command", {}))


if __name__ == "__main__":
    unittest.main()
