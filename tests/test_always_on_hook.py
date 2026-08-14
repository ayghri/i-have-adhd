import os
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "hooks" / "always-on.mjs"


class AlwaysOnHookTest(unittest.TestCase):
    def run_hook(self, config_dir):
        env = os.environ | {"CLAUDE_CONFIG_DIR": str(config_dir)}
        return subprocess.run(["node", HOOK], capture_output=True, text=True, env=env)

    def test_hook_is_silent_until_opted_in_then_emits_rules(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config_dir = Path(temp_dir)
            disabled = self.run_hook(config_dir)
            self.assertEqual((0, "", ""), (disabled.returncode, disabled.stdout, disabled.stderr))

            (config_dir / ".i-have-adhd-always").touch()
            enabled = self.run_hook(config_dir)
            self.assertEqual(0, enabled.returncode)
            self.assertEqual("", enabled.stderr)
            self.assertIn("ADHD MODE ACTIVE (always-on).", enabled.stdout)
            self.assertIn("# i-have-adhd", enabled.stdout)
            self.assertNotIn("\nname: i-have-adhd\n", enabled.stdout)

    def test_codex_plugin_names_match_the_marketplace_entry(self):
        marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
        expected_name = marketplace["plugins"][0]["name"]
        self.assertEqual(expected_name, marketplace["name"])
        for manifest in (ROOT / "plugin.json", ROOT / ".codex-plugin/plugin.json"):
            self.assertEqual(expected_name, json.loads(manifest.read_text())["name"])


if __name__ == "__main__":
    unittest.main()
