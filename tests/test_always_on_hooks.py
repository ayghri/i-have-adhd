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

    def opt_in(self):
        (self.config_dir / ".i-have-adhd-always").touch()

    def run_hook(self, command, **env_extra):
        env = os.environ.copy()
        env["CLAUDE_CONFIG_DIR"] = str(self.config_dir)
        for key in ("CLAUDE_PLUGIN_OPTION_ALWAYS_ON", "I_HAVE_ADHD_ALWAYS_ON"):
            env.pop(key, None)
        env.update(env_extra)
        return subprocess.run(
            [str(part) for part in command],
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )

    def run_codex_hook(self, plugin_root=None, **env_extra):
        config = json.loads((ROOT / "hooks" / "hooks.json").read_text())
        hook = config["hooks"]["SessionStart"][0]["hooks"][0]
        env = os.environ.copy()
        env["CLAUDE_CONFIG_DIR"] = str(self.config_dir)
        for key in ("CLAUDE_PLUGIN_OPTION_ALWAYS_ON", "I_HAVE_ADHD_ALWAYS_ON"):
            env.pop(key, None)
        env.update(env_extra)
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
        # The banner embeds the opt-out path. On Windows the sh runtime joins it
        # with "/" while node and PowerShell join with "\"; both name the same
        # file, so unify separators (and newlines) before comparing runtimes.
        return stdout.replace("\r\n", "\n").replace("\\", "/")

    def test_hook_is_silent_by_default(self):
        self.assertTrue(self.runtimes(), "no hook runtime is available")

        for name, command in self.runtimes():
            with self.subTest(runtime=name):
                result = self.run_hook(command)
                self.assertEqual(0, result.returncode)
                self.assertEqual("", result.stdout)
                self.assertEqual("", result.stderr)

    def assert_fires(self, result):
        self.assertEqual(0, result.returncode)
        self.assertEqual("", result.stderr)
        self.assertTrue(result.stdout.startswith("ADHD MODE ACTIVE (always-on)."))
        self.assertIn(".i-have-adhd-off", result.stdout)
        self.assertIn("## Rules", result.stdout)

    def test_hook_fires_with_the_flag_file(self):
        self.opt_in()
        for name, command in self.runtimes():
            with self.subTest(runtime=name):
                self.assert_fires(self.run_hook(command))

    def test_hook_fires_with_the_plugin_option(self):
        for value in ("true", "1", "YES", "on"):
            for name, command in self.runtimes():
                with self.subTest(runtime=name, value=value):
                    self.assert_fires(self.run_hook(command, CLAUDE_PLUGIN_OPTION_ALWAYS_ON=value))

    def test_hook_fires_with_the_environment_variable(self):
        for name, command in self.runtimes():
            with self.subTest(runtime=name):
                self.assert_fires(self.run_hook(command, I_HAVE_ADHD_ALWAYS_ON="1"))

    def test_plugin_option_false_keeps_the_hook_silent(self):
        for value in ("false", "0", "no", "off", ""):
            for name, command in self.runtimes():
                with self.subTest(runtime=name, value=value):
                    result = self.run_hook(command, CLAUDE_PLUGIN_OPTION_ALWAYS_ON=value)
                    self.assertEqual(0, result.returncode)
                    self.assertEqual("", result.stdout)

    def test_plugin_manifest_declares_the_always_on_option(self):
        manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
        option = manifest["userConfig"]["always_on"]
        self.assertEqual("boolean", option["type"])
        self.assertIs(False, option["default"])
        for key in ("title", "description"):
            self.assertTrue(option[key])

    def test_hook_is_silent_with_opt_out_flag(self):
        (self.config_dir / ".i-have-adhd-off").touch()
        self.opt_in()

        for name, command in self.runtimes():
            with self.subTest(runtime=name):
                result = self.run_hook(command)
                self.assertEqual(0, result.returncode)
                self.assertEqual("", result.stdout)
                self.assertEqual("", result.stderr)

    def test_hook_is_silent_when_output_style_is_selected(self):
        self.opt_in()
        for style in ("i-have-adhd", "i-have-adhd:i-have-adhd"):
            (self.config_dir / "settings.json").write_text(
                json.dumps({"model": "x", "outputStyle": style})
            )
            for name, command in self.runtimes():
                with self.subTest(runtime=name, style=style):
                    result = self.run_hook(command)
                    self.assertEqual(0, result.returncode)
                    self.assertEqual("", result.stdout)
                    self.assertEqual("", result.stderr)

    def test_hook_fires_when_another_output_style_is_selected(self):
        self.opt_in()
        (self.config_dir / "settings.json").write_text(
            json.dumps({"outputStyle": "Concise"})
        )
        for name, command in self.runtimes():
            with self.subTest(runtime=name):
                result = self.run_hook(command)
                self.assertEqual(0, result.returncode)
                self.assertTrue(result.stdout.startswith("ADHD MODE ACTIVE (always-on)."))

    def test_output_style_mirrors_the_skill_body(self):
        style = (ROOT / "output-styles" / "i-have-adhd.md").read_text()
        skill = (ROOT / "skills" / "i-have-adhd" / "SKILL.md").read_text()
        strip = lambda s: s.split("\n---\n", 1)[1].strip()
        self.assertIn("keep-coding-instructions: true", style.split("\n---\n", 1)[0])
        self.assertIn("\nname: i-have-adhd\n", style.split("\n---\n", 1)[0])
        self.assertEqual(strip(skill), strip(style))

    def test_session_start_matcher_includes_forked_sessions(self):
        config = json.loads((ROOT / "hooks" / "hooks.json").read_text())
        matcher = config["hooks"]["SessionStart"][0]["matcher"]
        self.assertEqual({"startup", "resume", "clear", "compact", "fork"}, set(matcher.split("|")))

    def test_opt_out_wins_over_every_opt_in(self):
        (self.config_dir / ".i-have-adhd-off").touch()
        self.opt_in()

        for name, command in self.runtimes():
            with self.subTest(runtime=name):
                result = self.run_hook(command, CLAUDE_PLUGIN_OPTION_ALWAYS_ON="true", I_HAVE_ADHD_ALWAYS_ON="1")
                self.assertEqual(0, result.returncode)
                self.assertEqual("", result.stdout)

    def test_runtimes_strip_frontmatter_with_trailing_whitespace(self):
        skill_path = self.plugin_root / "skills" / "i-have-adhd" / "SKILL.md"
        skill_path.write_text("---   \nname: fixture\n--- \t\nFixture body.\n")
        self.opt_in()
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
        self.opt_in()
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
        self.opt_in()
        result = self.run_codex_hook()

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("", result.stderr)
        self.assertIn("ADHD MODE ACTIVE (always-on)", result.stdout)

    def test_codex_command_is_silent_by_default(self):
        result = self.run_codex_hook()

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("", result.stderr)
        self.assertEqual("", result.stdout)

    def test_codex_command_honours_the_environment_variable(self):
        result = self.run_codex_hook(I_HAVE_ADHD_ALWAYS_ON="1")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("ADHD MODE ACTIVE (always-on)", result.stdout)

    def test_codex_command_is_silent_with_opt_out_flag(self):
        (self.config_dir / ".i-have-adhd-off").touch()
        self.opt_in()

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

    def run_node_hook_with_event(self, event_name, opt_out=False, **extra):
        self.opt_in()
        if opt_out:
            (self.config_dir / ".i-have-adhd-off").touch()
        node = shutil.which("node")
        self.assertTrue(node, "node is required for the event-shape tests")
        env = os.environ.copy()
        env["CLAUDE_CONFIG_DIR"] = str(self.config_dir)
        for key in ("CLAUDE_PLUGIN_OPTION_ALWAYS_ON", "I_HAVE_ADHD_ALWAYS_ON"):
            env.pop(key, None)
        return subprocess.run(
            [node, str(self.plugin_root / "hooks" / "always-on.mjs")],
            check=False,
            capture_output=True,
            text=True,
            env=env,
            input=json.dumps({"hook_event_name": event_name, "session_id": "t", **extra}),
        )

    def test_subagent_start_still_fires_when_output_style_is_selected(self):
        (self.config_dir / "settings.json").write_text(json.dumps({"outputStyle": "i-have-adhd"}))
        result = self.run_node_hook_with_event("SubagentStart", agent_type="Explore")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("ADHD MODE ACTIVE", json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"])

    def test_subagent_start_is_silent_for_fork_subagents(self):
        result = self.run_node_hook_with_event("SubagentStart", agent_type="fork")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("", result.stdout)

    def test_subagent_start_emits_additional_context_json(self):
        result = self.run_node_hook_with_event("SubagentStart")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("", result.stderr)
        payload = json.loads(result.stdout)
        output = payload["hookSpecificOutput"]
        self.assertEqual("SubagentStart", output["hookEventName"])
        self.assertIn("ADHD MODE ACTIVE", output["additionalContext"])
        self.assertIn("## Rules", output["additionalContext"])
        self.assertNotIn("name: i-have-adhd", output["additionalContext"])

    def test_subagent_start_is_silent_with_opt_out_flag(self):
        result = self.run_node_hook_with_event("SubagentStart", opt_out=True)

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("", result.stdout)

    def test_session_start_json_on_stdin_keeps_plain_banner(self):
        result = self.run_node_hook_with_event("SessionStart")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue(result.stdout.startswith("ADHD MODE ACTIVE (always-on)."))
        self.assertNotIn("hookSpecificOutput", result.stdout)

    def test_hooks_json_declares_subagent_start_with_the_same_launcher(self):
        config = json.loads((ROOT / "hooks" / "hooks.json").read_text())
        session = config["hooks"]["SessionStart"][0]["hooks"][0]["command"]
        subagent_entries = config["hooks"]["SubagentStart"]

        self.assertEqual(1, len(subagent_entries))
        self.assertNotIn("matcher", subagent_entries[0])
        self.assertEqual(session, subagent_entries[0]["hooks"][0]["command"])


if __name__ == "__main__":
    unittest.main()
