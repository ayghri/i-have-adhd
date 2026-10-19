import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

# Exercise both runtime APIs against the same fixtures.
INJECTION_MODES = ["context", "v1-context"]


@unittest.skipUnless(shutil.which("node"), "node is required for the OpenCode plugin")
class OpenCodePluginTest(unittest.TestCase):
    """Mirror tests/test_always_on_hooks.py for the OpenCode server plugin: the
    always-on flag gates injection, and frontmatter stripping matches the hooks.

    V2 registers through `ctx.skill.transform` and `ctx.command.transform`; V1
    mutates the config object in its `config` hook. Both paths are covered."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.plugin_root = Path(self.temp_dir.name).resolve() / "plugin"
        shutil.copytree(ROOT / ".opencode", self.plugin_root / ".opencode")
        shutil.copytree(ROOT / "skills", self.plugin_root / "skills")
        # The plugin reads its flag from $XDG_CONFIG_HOME/opencode/.i-have-adhd-always.
        self.config_dir = Path(self.temp_dir.name) / "config"
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

    # --- always-on injection, asserted through both APIs ---

    def test_silent_without_opt_in_flag(self):
        for mode in INJECTION_MODES:
            with self.subTest(mode=mode):
                result = self.run_plugin(mode)
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual("", result.stdout)

    def test_injects_ruleset_when_opted_in(self):
        self.opt_in()
        for mode in INJECTION_MODES:
            with self.subTest(mode=mode):
                result = self.run_plugin(mode)
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertIn("ADHD MODE ACTIVE (always-on)", result.stdout)
                self.assertIn("Working memory is small", result.stdout)

    def test_strips_frontmatter_with_trailing_whitespace(self):
        self.write_skill("---   \nname: fixture\n--- \t\nFixture body.\n")
        self.opt_in()
        for mode in INJECTION_MODES:
            with self.subTest(mode=mode):
                result = self.run_plugin(mode)
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertNotIn("name: fixture", result.stdout)
                self.assertIn("\n\nFixture body.", result.stdout)

    def test_keeps_content_when_frontmatter_is_unclosed(self):
        self.write_skill("---\nname: fixture\nFixture body, fence never closed.\n")
        self.opt_in()
        for mode in INJECTION_MODES:
            with self.subTest(mode=mode):
                result = self.run_plugin(mode)
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertIn("Fixture body, fence never closed.", result.stdout)

    def test_both_apis_share_the_same_injected_text(self):
        self.opt_in()
        v2 = self.run_plugin("context").stdout
        v1 = self.run_plugin("v1-context").stdout
        self.assertEqual(v2, v1)

    # --- V2 registration ---

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

    # --- V1 config registration ---

    def test_v1_config_hook_registers_the_slash_command(self):
        result = self.run_plugin(mode="v1-config")
        self.assertEqual(0, result.returncode, result.stderr)
        config = json.loads(result.stdout)
        command = config["command"]["i-have-adhd"]
        self.assertIn("ADHD", command["description"])
        self.assertIn("stop adhd mode", command["template"])

    def test_v1_config_hook_registers_the_skills_path(self):
        result = self.run_plugin(mode="v1-config")
        self.assertEqual(0, result.returncode, result.stderr)
        config = json.loads(result.stdout)
        self.assertIn(str(self.plugin_root / "skills"), config["skills"]["paths"])

    def test_v1_config_preserves_existing_command(self):
        custom = {"description": "User command", "template": "Keep this", "agent": "plan"}
        result = self.run_plugin("v1-config", {"command": {"i-have-adhd": custom}})
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(custom, json.loads(result.stdout)["command"]["i-have-adhd"])

    def test_v1_repeated_config_does_not_duplicate_skill_paths(self):
        result = self.run_plugin("v1-config")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(
            [str(self.plugin_root / "skills")], json.loads(result.stdout)["skills"]["paths"]
        )

    def test_v1_command_preserves_metadata_and_trims_template(self):
        metadata = {"description": 'ADHD: "focus"\nnext line', "agent": "plan",
                    "model": "fixture/model", "subagent": True}
        command = self.plugin_root / ".opencode/command/i-have-adhd.md"
        command.write_bytes(("---  \r\n" + json.dumps(metadata) +
                             "\r\n--- \t\r\n\r\nUse the skill.\r\n\r\n").encode())
        result = self.run_plugin("v1-config")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual({**metadata, "template": "Use the skill."},
                         json.loads(result.stdout)["command"]["i-have-adhd"])

    def test_v1_missing_command_keeps_skill_discovery(self):
        (self.plugin_root / ".opencode/command/i-have-adhd.md").unlink()
        result = self.run_plugin("v1-config")
        self.assertEqual(0, result.returncode, result.stderr)
        config = json.loads(result.stdout)
        self.assertNotIn("i-have-adhd", config["command"])
        self.assertEqual([str(self.plugin_root / "skills")], config["skills"]["paths"])

    def test_v1_malformed_command_does_not_leak_frontmatter_into_prompt(self):
        command = self.plugin_root / ".opencode/command/i-have-adhd.md"
        for text in ["---\n{broken}\n---\nBody", '---\n{"description":"unclosed"}\nBody']:
            with self.subTest(text=text):
                command.write_text(text)
                result = self.run_plugin("v1-config")
                self.assertEqual(0, result.returncode, result.stderr)
                config = json.loads(result.stdout)
                self.assertNotIn("i-have-adhd", config["command"])
                self.assertEqual([str(self.plugin_root / "skills")], config["skills"]["paths"])


    def test_js_mirror_reexports_the_implementation(self):
        # Discovery uses .js; re-exporting must preserve the module identity.
        mirror = ROOT / ".opencode" / "plugins" / "i-have-adhd.js"
        impl = ROOT / ".opencode" / "plugins" / "i-have-adhd.mjs"
        self.assertTrue(mirror.is_file(), "missing V2 auto-discovery mirror")
        self.assertTrue(impl.is_file())

        env = os.environ.copy()
        env["XDG_CONFIG_HOME"] = str(self.config_dir)
        script = (
            "const a = (await import(process.argv[1])).default;"
            "const b = (await import(process.argv[2])).default;"
            "process.stdout.write(JSON.stringify({"
            "same: a === b,"
            "id: a.id, keys: Object.keys(a).sort()}));"
        )
        result = subprocess.run(
            ["node", "--input-type=module", "-e", script, mirror.as_uri(), impl.as_uri()],
            check=False, capture_output=True, text=True, env=env,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        mirror_export = json.loads(result.stdout)
        self.assertTrue(mirror_export["same"], "mirror does not re-export the implementation")
        self.assertEqual("i-have-adhd", mirror_export["id"])
        self.assertEqual(["id", "server", "setup"], mirror_export["keys"])


if __name__ == "__main__":
    unittest.main()
