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


class AlwaysOnSnippetTest(unittest.TestCase):
    # The pasted always-on snippets and the Gemini command are condensed copies
    # of SKILL.md. They must keep its off-switch, and the English snippet must
    # keep rule 9 presentation-only (#96) rather than a bare "cap at 5".
    def rule_blocks(self, path):
        text = path.read_text(encoding="utf8")
        blocks = re.findall(r"```markdown\n(.*?)```", text, re.S)
        return [block for block in blocks if re.search(r"^10\. ", block, re.M)]

    def test_snippets_keep_off_switch(self):
        translations = sorted((ROOT / ".github/install").glob("INSTALL.*.md"))
        self.assertTrue(translations, "No translated installation guides found")
        for path in [ROOT / "INSTALL.md", *translations]:
            with self.subTest(file=path.name):
                blocks = self.rule_blocks(path)
                self.assertTrue(blocks, "No always-on rule snippets found")
                for block in blocks:
                    self.assertIn("stop adhd mode", block)
                    self.assertIn("normal mode", block)

    def test_english_snippet_rule_9_is_presentation_only(self):
        for block in self.rule_blocks(ROOT / "INSTALL.md"):
            self.assertIn("presentation only", block)
            self.assertNotIn("9. Cap lists to 5 items.\n", block)

    def test_gemini_command_keeps_off_switch(self):
        text = (ROOT / "skills/i-have-adhd/agents/gemini.toml").read_text(encoding="utf8")
        self.assertIn("stop adhd mode", text)
        self.assertIn("normal mode", text)


if __name__ == "__main__":
    unittest.main()
