import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COPILOT_DIR = ROOT / "com.github.copilot"
FLAG_NAME = ".i-have-adhd-always"


class CopilotManifestTest(unittest.TestCase):
    """The root plugin.json is the Agent Plugins 1.0 manifest VS Code reads."""

    def test_root_manifest_declares_agent_plugins_schema(self):
        manifest = json.loads((ROOT / "plugin.json").read_text())
        self.assertEqual(
            "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
            manifest["$schema"],
        )

    def test_plugin_name_is_portable(self):
        manifest = json.loads((ROOT / "plugin.json").read_text())
        name = manifest["name"]
        self.assertEqual("i-have-adhd", name)
        # Agent Plugins 1.0 constrains names so they can double as directory
        # and identifier: plain lowerscore-free kebab-case, no doubled separators.
        self.assertRegex(name, r"^[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")
        self.assertNotIn("--", name)
        self.assertNotIn("..", name)

    def test_versions_stay_aligned_with_the_claude_manifest(self):
        root_manifest = json.loads((ROOT / "plugin.json").read_text())
        claude_manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
        self.assertEqual(root_manifest["version"], claude_manifest["version"])
        self.assertEqual(root_manifest["name"], claude_manifest["name"])


class CopilotHookDeclarationTest(unittest.TestCase):
    """com.github.copilot/hooks/hooks.json declares the opt-in sessionStart hook."""

    def setUp(self):
        self.config = json.loads((COPILOT_DIR / "hooks" / "hooks.json").read_text())

    def test_declares_a_single_session_start_command(self):
        self.assertEqual(1, self.config["version"])
        self.assertEqual(["sessionStart"], list(self.config["hooks"]))
        (hook,) = self.config["hooks"]["sessionStart"]
        self.assertEqual("command", hook["type"])

    def test_command_launches_the_shared_node_hook_from_the_plugin_root(self):
        (hook,) = self.config["hooks"]["sessionStart"]
        command = hook["command"]
        self.assertIn("node", command)
        self.assertIn("${PLUGIN_ROOT}/hooks/always-on.mjs", command)
        # A hardcoded path away from ${PLUGIN_ROOT} would break installs that
        # clone the repository elsewhere.
        self.assertNotIn("${CLAUDE_PLUGIN_ROOT}", command)

    def test_marks_the_session_as_copilot(self):
        (hook,) = self.config["hooks"]["sessionStart"]
        self.assertEqual("copilot", hook["env"]["I_HAVE_ADHD_CLIENT"])
        self.assertIsInstance(hook.get("timeoutSec"), int)
        self.assertLess(hook["timeoutSec"], 60)

    def test_provides_the_slash_command_file(self):
        text = (COPILOT_DIR / "commands" / "i-have-adhd.md").read_text()
        self.assertTrue(text.startswith("---\n"))
        parts = text.split("---\n", 2)
        self.assertIn("description:", parts[1])
        self.assertIn("i-have-adhd", parts[2])
        self.assertIn("stop adhd mode", parts[2])


class CopilotAlwaysOnHookTest(unittest.TestCase):
    """Within a Copilot session the hook reads the Copilot config home only."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.plugin_root = Path(self.temp_dir.name) / "plugin with spaces"
        shutil.copytree(ROOT / "hooks", self.plugin_root / "hooks")
        shutil.copytree(ROOT / "skills", self.plugin_root / "skills")
        self.copilot_home = Path(self.temp_dir.name) / "copilot home"
        self.copilot_home.mkdir()
        self.claude_home = Path(self.temp_dir.name) / "claude config"
        self.claude_home.mkdir()
        self.default_home = Path(self.temp_dir.name) / "default home"
        (self.default_home / ".copilot").mkdir(parents=True)

    def run_hook(self, as_copilot=True, copilot_home=True, claude_config_dir=None):
        node = shutil.which("node")
        if node is None:
            self.skipTest("node is not available")
        env = os.environ.copy()
        env.pop("I_HAVE_ADHD_CLIENT", None)
        if as_copilot:
            env["I_HAVE_ADHD_CLIENT"] = "copilot"
        if claude_config_dir is None:
            # Keep the Claude opt-out contract intact for other sessions while
            # pinning every Copilot lookup to throwaway homes.
            env.pop("CLAUDE_CONFIG_DIR", None)
        else:
            env["CLAUDE_CONFIG_DIR"] = str(claude_config_dir)
        env["HOME"] = str(self.default_home)
        env["USERPROFILE"] = str(self.default_home)
        if copilot_home:
            env["COPILOT_HOME"] = str(self.copilot_home)
        else:
            env.pop("COPILOT_HOME", None)
        return subprocess.run(
            [node, str(self.plugin_root / "hooks" / "always-on.mjs")],
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )

    @staticmethod
    def normalize(stdout):
        # The banner embeds the flag path; unify separators like the shared
        # hook tests so assertions hold on Windows too.
        return stdout.replace("\r\n", "\n").replace("\\", "/")

    def test_is_silent_without_the_opt_in_flag(self):
        result = self.run_hook()
        self.assertEqual(0, result.returncode)
        self.assertEqual("", result.stdout)
        self.assertEqual("", result.stderr)

    def test_prints_the_ruleset_when_the_copilot_flag_exists(self):
        (self.copilot_home / FLAG_NAME).touch()
        result = self.run_hook()
        self.assertEqual(0, result.returncode)
        self.assertEqual("", result.stderr)
        normalized = self.normalize(result.stdout)
        self.assertIn("ADHD MODE ACTIVE", normalized)
        # Frontmatter must be stripped from the injected skill body.
        self.assertNotIn("name:", normalized)
        self.assertIn(str(self.copilot_home).replace("\\", "/"), normalized)

    def test_ignores_a_claude_opt_in_flag(self):
        # The Claude flag must not activate Copilot sessions, even when the
        # hook is pointed straight at the Claude config dir, so one runtime's
        # opt-in never leaks into the other.
        (self.claude_home / FLAG_NAME).touch()
        env_result = self.run_hook(claude_config_dir=self.claude_home)
        self.assertEqual(0, env_result.returncode)
        self.assertEqual("", env_result.stdout)

    def test_claude_sessions_still_use_the_claude_config_dir(self):
        (self.claude_home / FLAG_NAME).touch()
        node = shutil.which("node")
        if node is None:
            self.skipTest("node is not available")
        env = os.environ.copy()
        env.pop("I_HAVE_ADHD_CLIENT", None)
        env["CLAUDE_CONFIG_DIR"] = str(self.claude_home)
        result = subprocess.run(
            [node, str(self.plugin_root / "hooks" / "always-on.mjs")],
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertEqual(0, result.returncode)
        self.assertIn("ADHD MODE ACTIVE", self.normalize(result.stdout))

    def test_falls_back_to_copilot_home_default(self):
        # With COPILOT_HOME unset the hook uses <home>/.copilot; flagging it
        # there activates the session under the hermetic default home.
        (self.default_home / ".copilot" / FLAG_NAME).touch()
        result = self.run_hook(copilot_home=False)
        self.assertEqual(0, result.returncode)
        self.assertEqual("", result.stderr)
        self.assertIn("ADHD MODE ACTIVE", self.normalize(result.stdout))


class CopilotInstallDocsTest(unittest.TestCase):
    """INSTALL.md documents the plugin route before the skill-only fallback."""

    def setUp(self):
        text = (ROOT / "INSTALL.md").read_text()
        marker = "<summary><strong>GitHub Copilot (VS Code and Copilot CLI)</strong></summary>"
        self.section = text.split(marker, 1)[1].split("</details>", 1)[0]

    def test_documents_vscode_and_cli_install_commands(self):
        self.assertIn("/plugin install https://github.com/ayghri/i-have-adhd", self.section)
        self.assertIn("copilot plugin install ayghri/i-have-adhd", self.section)

    def test_documents_copilot_scoped_always_on_flag(self):
        self.assertIn("touch ~/.copilot/.i-have-adhd-always", self.section)
        self.assertIn("COPILOT_HOME", self.section)
        self.assertIn("copilot plugin update i-have-adhd", self.section)
        self.assertIn("copilot plugin uninstall i-have-adhd", self.section)

    def test_plugin_route_is_listed_before_the_skill_only_fallback(self):
        plugin_index = self.section.index("/plugin install https://github.com/ayghri/i-have-adhd")
        skills_index = self.section.index("npx skills add ayghri/i-have-adhd -a github-copilot")
        self.assertLess(plugin_index, skills_index)


if __name__ == "__main__":
    unittest.main()
