import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
QODER_MANIFEST = ROOT / ".qoder-plugin" / "plugin.json"


class QoderPluginTest(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads(QODER_MANIFEST.read_text(encoding="utf8"))
        self.package = json.loads((ROOT / "package.json").read_text(encoding="utf8"))

    def test_manifest_exposes_canonical_skill(self):
        self.assertEqual("i-have-adhd", self.manifest["name"])
        self.assertEqual("./skills/", self.manifest["skills"])
        self.assertTrue(ROOT.joinpath(self.manifest["skills"]).is_dir())
        self.assertTrue(ROOT.joinpath("skills/i-have-adhd/SKILL.md").is_file())

    def test_manifest_metadata_matches_shared_package(self):
        for field in ("name", "version", "license", "homepage"):
            with self.subTest(field=field):
                self.assertEqual(self.package[field], self.manifest[field])

    def test_qoder_zip_contains_manifest_and_canonical_skill(self):
        with tempfile.TemporaryDirectory(prefix="i-have-adhd-qoder-") as output_dir:
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/package_qoder_plugin.py"),
                    "--output-dir",
                    output_dir,
                ],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            archive_path = Path(result.stdout.strip())
            self.assertTrue(archive_path.is_file())
            with ZipFile(archive_path) as archive:
                names = set(archive.namelist())
            self.assertIn(".qoder-plugin/plugin.json", names)
            self.assertIn("skills/i-have-adhd/SKILL.md", names)
            self.assertNotIn(".cursor/skills/i-have-adhd/SKILL.md", names)


if __name__ == "__main__":
    unittest.main()
