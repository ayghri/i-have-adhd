"""Checks installation paths in INSTALL.md and translations."""

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


class GrokInstallPathTest(unittest.TestCase):
    def test_grok_install_commands(self):
        text = (ROOT / "INSTALL.md").read_text(encoding="utf8")
        marker = "<summary><strong>Grok (<code>grok</code>)</strong></summary>"
        self.assertIn(marker, text)
        section = text.split(marker, 1)[1]
        self.assertIn("</details>", section)
        section = section.split("</details>", 1)[0]

        self.assertIn("grok plugin marketplace add ayghri/i-have-adhd", section)
        self.assertIn("grok plugin install ayghri/i-have-adhd --trust", section)
        self.assertIn("grok plugin enable i-have-adhd", section)
        self.assertIn("grok plugin update i-have-adhd", section)
        self.assertIn("grok plugin uninstall i-have-adhd --confirm", section)
        self.assertIn("grok plugin marketplace remove i-have-adhd", section)
        self.assertIn("/i-have-adhd", section)
        self.assertIn("~/.grok/AGENTS.md", section)
        self.assertIn("~/.grok/rules/i-have-adhd.md", section)
        self.assertNotIn("~/.claude/.i-have-adhd-always", section)


if __name__ == "__main__":
    unittest.main()
