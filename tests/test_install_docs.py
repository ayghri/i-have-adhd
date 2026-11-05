"""Checks installation paths in INSTALL.md and translations."""

import pathlib
import re
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class ClaudeCodeUpdateTest(unittest.TestCase):
    def test_marketplace_refresh_is_paired_with_plugin_update(self):
        # `claude plugin marketplace update` refreshes only the marketplace
        # listing; the installed copy stays at its old version until
        # `claude plugin update` runs, so the docs must never offer the first alone.
        refresh = "claude plugin marketplace update i-have-adhd"
        update = "claude plugin update i-have-adhd@i-have-adhd"
        translations = sorted((ROOT / ".github/install").glob("INSTALL.*.md"))
        self.assertTrue(translations, "No translated installation guides found")
        for path in [ROOT / "INSTALL.md", *translations]:
            with self.subTest(file=path.name):
                text = path.read_text(encoding="utf8")
                self.assertIn(update, text)
                for block in re.split(r"\n[^\S\n]*\n", text):
                    if refresh in block:
                        self.assertIn(update, block)


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


class MuseInstallPathTest(unittest.TestCase):
    def test_muse_install_does_not_rebind_a_different_source(self):
        text = (ROOT / "INSTALL.md").read_text(encoding="utf8")
        marker = "<summary><strong>Muse Code (<code>muse</code>)</strong></summary>"
        section = text.split(marker, 1)[1].split("</details>", 1)[0]
        all_installs = re.findall(r"^muse plugins install .*", section, re.MULTILINE)
        self.assertTrue(all("--scope" not in command for command in all_installs))
        self.assertIn("muse plugins install i-have-adhd@i-have-adhd", all_installs)
        installs = [command for command in all_installs if '"$HOME/.local/share/i-have-adhd"' in command]
        self.assertEqual(3, len(installs))
        self.assertIn(
            'git clone https://github.com/ayghri/i-have-adhd.git '
            '"$HOME/.local/share/i-have-adhd" &&\n' + installs[0],
            section,
        )
        self.assertIn(
            'git -C "$HOME/.local/share/i-have-adhd" pull --ff-only &&\n' + installs[2],
            section,
        )
        self.assertIn("muse plugins approve '<stable-id>'", section)
        self.assertIn("including its `plugin:` prefix", section)


class GrokInstallPathTest(unittest.TestCase):
    def test_grok_install_commands(self):
        text = (ROOT / "INSTALL.md").read_text(encoding="utf8")
        marker = "<summary><strong>Grok (<code>grok</code>)</strong></summary>"
        self.assertIn(marker, text)
        section = text.split(marker, 1)[1]
        self.assertIn("</details>", section)
        section = section.split("</details>", 1)[0]

        self.assertIn("grok plugin install ayghri/i-have-adhd --trust", section)
        self.assertIn("grok plugin enable i-have-adhd", section)
        self.assertIn("grok plugin update i-have-adhd", section)
        self.assertIn("grok plugin uninstall i-have-adhd --confirm", section)
        self.assertIn("/i-have-adhd", section)
        self.assertIn("~/.grok/AGENTS.md", section)
        self.assertIn("~/.grok/rules/i-have-adhd.md", section)
        self.assertNotIn("~/.claude/.i-have-adhd-always", section)


if __name__ == "__main__":
    unittest.main()
