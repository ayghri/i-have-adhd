import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class AntigravityHookTest(unittest.TestCase):
    def test_opt_in_injects_canonical_rules_and_default_is_empty(self):
        with tempfile.TemporaryDirectory() as temp:
            env = {**os.environ, "HOME": temp, "USERPROFILE": temp}
            def run():
                return json.loads(subprocess.run(
                    ["node", str(ROOT / "hooks/agy-always-on.mjs")],
                    input="{}", text=True, capture_output=True, check=True, env=env,
                ).stdout)
            self.assertEqual(run(), {})
            claude_flag = Path(temp) / ".claude/.i-have-adhd-always"
            claude_flag.parent.mkdir()
            claude_flag.touch()
            self.assertEqual(run(), {})
            flag = Path(temp) / ".gemini/antigravity-cli/.i-have-adhd-always"
            flag.parent.mkdir(parents=True)
            flag.touch()
            output = run()["injectSteps"][0]["userMessage"]
            self.assertIn("The reader has ADHD.", output)
            self.assertIn("stop adhd mode", output)
            flag.unlink()
            self.assertEqual(run(), {})

if __name__ == "__main__":
    unittest.main()
