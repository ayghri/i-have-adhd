import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
QODER_MANIFEST = ROOT / ".qoder-plugin" / "plugin.json"


def find_qoder_cli():
    """Avoid mistaking the Qoder IDE launcher for the Qoder agent CLI."""
    for name in ("qodercli", "qoder"):
        executable = shutil.which(name)
        if not executable:
            continue
        result = subprocess.run(
            [executable, "plugins", "--help"],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0 and "Manage plugins" in result.stdout:
            return executable
    return None


QODER_EXECUTABLE = find_qoder_cli()


class QoderPluginTest(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads(QODER_MANIFEST.read_text(encoding="utf8"))
        self.package = json.loads((ROOT / "package.json").read_text(encoding="utf8"))

    def test_manifest_exposes_canonical_skill(self):
        self.assertEqual("i-have-adhd", self.manifest["name"])
        self.assertEqual("./skills/", self.manifest["skills"])
        self.assertTrue(ROOT.joinpath(self.manifest["skills"]).is_dir())
        self.assertTrue(ROOT.joinpath("skills/i-have-adhd/SKILL.md").is_file())
        self.assertEqual("./hooks/hooks.json", self.manifest["hooks"])
        self.assertTrue(ROOT.joinpath(self.manifest["hooks"]).is_file())

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
            self.assertIn("hooks/hooks.json", names)
            self.assertIn("hooks/always-on.mjs", names)
            self.assertIn("hooks/always-on.sh", names)
            self.assertIn("hooks/always-on.ps1", names)
            self.assertNotIn(".cursor/skills/i-have-adhd/SKILL.md", names)

    @unittest.skipUnless(
        QODER_EXECUTABLE,
        "qoder or qodercli is required for native plugin validation",
    )
    def test_qoder_cli_validates_installs_and_lists_plugin(self):
        with tempfile.TemporaryDirectory(
            prefix="i-have-adhd-qoder-config-",
        ) as config_dir:
            command = [QODER_EXECUTABLE, "--config-dir", config_dir]
            subprocess.run(
                [*command, "plugins", "validate", str(ROOT)],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [*command, "plugins", "install", str(ROOT)],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            listed = subprocess.run(
                [*command, "plugins", "list", "--json"],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            plugins = json.loads(listed.stdout)
            plugin = next(
                item for item in plugins if item["name"] == "i-have-adhd"
            )
            self.assertTrue(plugin["enabled"])
            self.assertEqual(
                ["i-have-adhd"],
                [skill["name"] for skill in plugin["resources"]["skills"]],
            )
            self.assertIn(
                {
                    "event": "SessionStart",
                    "matcher": "startup|resume|clear|compact",
                    "type": "command",
                },
                plugin["resources"]["hooks"],
            )
            skills = subprocess.run(
                [*command, "skills", "list", "--all"],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("i-have-adhd", skills.stdout)


if __name__ == "__main__":
    unittest.main()
