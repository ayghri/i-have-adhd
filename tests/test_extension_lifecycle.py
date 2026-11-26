"""Run the isolated actual-extension host tests without installing a runtime."""

import shutil
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ExtensionLifecycleTest(unittest.TestCase):
    def test_pi_and_omp_session_lifecycle(self):
        node = shutil.which("node")
        if node is None:
            self.skipTest("Node 22.18+ is required for TypeScript module hooks")
        version = subprocess.run([node, "--version"], check=True, capture_output=True,
                                 text=True, timeout=10).stdout.strip().lstrip("v")
        if tuple(int(part) for part in version.split(".")) < (22, 18, 0):
            self.skipTest("Node 22.18+ is required for TypeScript module hooks")
        result = subprocess.run([node, "--test", "tests/extension_lifecycle.test.mjs"],
                                cwd=ROOT, capture_output=True, text=True,
                                encoding="utf-8", timeout=30)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
