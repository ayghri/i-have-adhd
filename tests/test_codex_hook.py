import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CodexHookTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.plugin_root = Path(self.temp_dir.name) / "plugin with spaces"
        shutil.copytree(ROOT / "hooks", self.plugin_root / "hooks")
        shutil.copytree(ROOT / "skills", self.plugin_root / "skills")
        self.config_dir = Path(self.temp_dir.name) / "claude config"
        self.config_dir.mkdir()

    def run_hook(self, plugin_root=None):
        manifest = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text())
        config = json.loads((ROOT / manifest.get("hooks", "hooks/hooks.json")).read_text())
        command = config["hooks"]["SessionStart"][0]["hooks"][0]["command"]
        env = os.environ.copy()
        env.update(CLAUDE_CONFIG_DIR=str(self.config_dir),
                   CLAUDE_PLUGIN_ROOT=str(plugin_root or self.plugin_root),
                   PLUGIN_ROOT=str(plugin_root or self.plugin_root))
        return subprocess.run(command, shell=True, env=env, capture_output=True,
                              text=True, encoding="utf-8", timeout=10,
                              input=json.dumps({"hook_event_name": "SessionStart", "source": "startup",
                                                "cwd": str(self.plugin_root), "session_id": "test-session"}))

    def test_codex_receives_the_complete_context_in_a_json_envelope(self):
        (self.config_dir / ".i-have-adhd-always").touch()
        skill = self.plugin_root / "skills" / "i-have-adhd" / "SKILL.md"
        skill.write_bytes(skill.read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
        result = self.run_hook()
        self.assertEqual((0, ""), (result.returncode, result.stderr))
        output = json.loads(result.stdout)["hookSpecificOutput"]
        self.assertEqual("SessionStart", output["hookEventName"])
        env = os.environ.copy()
        env["CLAUDE_CONFIG_DIR"] = str(self.config_dir)
        plain = subprocess.run([shutil.which("node"), self.plugin_root / "hooks" / "always-on.mjs"],
                               env=env, capture_output=True, timeout=10)
        self.assertEqual(0, plain.returncode, plain.stderr)
        plain_context = plain.stdout.decode("utf-8")
        self.assertTrue(plain_context.startswith("ADHD MODE ACTIVE (always-on)"))
        self.assertEqual(plain_context, output["additionalContext"])
        self.assertNotIn("metadata:", output["additionalContext"])

    def test_codex_is_silent_without_opt_in(self):
        result = self.run_hook()
        self.assertEqual((0, "", ""), (result.returncode, result.stdout, result.stderr))

    def test_codex_is_silent_when_skill_is_missing(self):
        (self.config_dir / ".i-have-adhd-always").touch()
        shutil.rmtree(self.plugin_root / "skills")
        result = self.run_hook()
        self.assertEqual((0, "", ""), (result.returncode, result.stdout, result.stderr))

    def test_codex_is_silent_when_plugin_is_missing(self):
        result = self.run_hook(self.plugin_root / "missing plugin")
        self.assertEqual((0, "", ""), (result.returncode, result.stdout, result.stderr))
