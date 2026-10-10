import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile


ROOT = pathlib.Path(__file__).resolve().parents[1]
QODER_MANIFEST = ROOT / ".qoder-plugin" / "plugin.json"


def find_qoder_cli(config_dir):
    """Avoid mistaking the Qoder IDE launcher for the Qoder agent CLI."""
    for name in ("qodercli", "qoder"):
        executable = shutil.which(name)
        if not executable:
            continue
        result = subprocess.run(
            [executable, "--config-dir", config_dir, "plugins", "--help"],
            timeout=30,
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0 and "Manage plugins" in result.stdout:
            return executable
    return None


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

    def test_qoder_always_on_hook_executes_for_new_sessions(self):
        hooks = json.loads(
            ROOT.joinpath(self.manifest["hooks"]).read_text(encoding="utf8")
        )["hooks"]["SessionStart"][0]
        self.assertIn("new", hooks["matcher"].split("|"))

        with tempfile.TemporaryDirectory(
            prefix="i-have-adhd-qoder-hook-",
        ) as config_dir:
            pathlib.Path(config_dir, ".i-have-adhd-always").touch()
            env = {
                **os.environ,
                "QODER_PLUGIN_ROOT": str(ROOT),
                "QODER_CONFIG_DIR": config_dir,
            }
            result = subprocess.run(
                hooks["hooks"][0]["command"],
                cwd=ROOT,
                env=env,
                shell=True,
                timeout=30,
                check=True,
                capture_output=True,
                text=True,
            )

        self.assertIn("ADHD MODE ACTIVE (always-on)", result.stdout)
        self.assertIn("Lead with the next action", result.stdout)

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
                timeout=30,
                check=True,
                capture_output=True,
                text=True,
            )
            archive_path = pathlib.Path(result.stdout.strip())
            self.assertTrue(archive_path.is_file())
            with zipfile.ZipFile(archive_path) as archive:
                names = set(archive.namelist())
            self.assertIn(".qoder-plugin/plugin.json", names)
            self.assertIn("skills/i-have-adhd/SKILL.md", names)
            self.assertIn("hooks/hooks.json", names)
            self.assertIn("hooks/always-on.mjs", names)
            self.assertIn("hooks/always-on.sh", names)
            self.assertIn("hooks/always-on.ps1", names)
            self.assertNotIn(".cursor/skills/i-have-adhd/SKILL.md", names)

    def test_qoder_cli_validates_installs_and_lists_plugin(self):
        with tempfile.TemporaryDirectory(
            prefix="i-have-adhd-qoder-config-",
        ) as config_dir:
            executable = find_qoder_cli(config_dir)
            if not executable:
                self.skipTest("qoder or qodercli is required for native validation")
            command = [executable, "--config-dir", config_dir]
            subprocess.run(
                [*command, "plugins", "validate", str(ROOT)],
                cwd=ROOT,
                timeout=30,
                check=True,
                capture_output=True,
                text=True,
            )
            subprocess.run(
                [*command, "plugins", "install", str(ROOT)],
                cwd=ROOT,
                timeout=30,
                check=True,
                capture_output=True,
                text=True,
            )
            listed = subprocess.run(
                [*command, "plugins", "list", "--json"],
                cwd=ROOT,
                timeout=30,
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
                    "matcher": "startup|resume|clear|compact|new",
                    "type": "command",
                },
                plugin["resources"]["hooks"],
            )
            skills = subprocess.run(
                [*command, "skills", "list", "--all"],
                cwd=ROOT,
                timeout=30,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("i-have-adhd", skills.stdout)


if __name__ == "__main__":
    unittest.main()
