"""Checks platform installation paths across the installation guides."""

import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class ZedInstallPathTest(unittest.TestCase):
    def test_zed_install_paths(self):
        translations = sorted((ROOT / ".github/install").glob("INSTALL.*.md"))
        self.assertTrue(translations, "No translated installation guides found")
        for path in [ROOT / "INSTALL.md", *translations]:
            with self.subTest(file=path.name):
                text = path.read_text(encoding="utf8")
                marker = "<summary><strong>Zed</strong></summary>"
                self.assertIn(marker, text)
                section = text.split(marker, 1)[1]
                self.assertIn("</details>", section)
                section = section.split("</details>", 1)[0]

                self.assertNotIn("~/.config/zed/skills", section)
                self.assertIn(
                    "mkdir -p ~/.agents/skills\n"
                    "cp -R i-have-adhd/skills/i-have-adhd ~/.agents/skills/",
                    section,
                )
                self.assertIn("~/.agents/skills/i-have-adhd", section)


class QoderInstallDocsTest(unittest.TestCase):
    def test_qoder_install_and_lifecycle_are_documented(self):
        translations = sorted((ROOT / ".github/install").glob("INSTALL.*.md"))
        for path in [ROOT / "INSTALL.md", *translations]:
            with self.subTest(file=path.name):
                text = path.read_text(encoding="utf8")
                self.assertRegex(
                    text,
                    r"<summary><strong>Qoder IDE (?:and|e|và|및|和|/) Qoder CLI</strong></summary>",
                )
                self.assertIn("qoder plugins validate ./i-have-adhd", text)
                self.assertIn("qoder plugins install ./i-have-adhd", text)
                self.assertIn("qoder plugins list", text)
                self.assertIn("qoder plugins uninstall i-have-adhd", text)
                self.assertIn(
                    "python3 i-have-adhd/scripts/package_qoder_plugin.py",
                    text,
                )
                self.assertIn(
                    "i-have-adhd/dist/qoder/i-have-adhd-0.3.0.zip",
                    text,
                )
                self.assertIn(
                    'touch "${QODER_CONFIG_DIR:-$HOME/.qoder}/.i-have-adhd-always"',
                    text,
                )
                self.assertIn(
                    'rm "${QODER_CONFIG_DIR:-$HOME/.qoder}/.i-have-adhd-always"',
                    text,
                )
                self.assertIn("/i-have-adhd", text)


if __name__ == "__main__":
    unittest.main()
