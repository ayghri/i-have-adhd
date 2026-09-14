"""Validates Google Antigravity integration, skill mirroring, and docs."""

import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class AntigravityIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.canonical_skill = ROOT / "skills" / "i-have-adhd" / "SKILL.md"
        self.agents_skill = ROOT / ".agents" / "skills" / "i-have-adhd" / "SKILL.md"
        self.install_md = ROOT / "INSTALL.md"
        self.agents_md = ROOT / "AGENTS.md"

    def test_agents_skill_mirror_synchronized(self):
        self.assertTrue(
            self.agents_skill.is_file(),
            f"Missing .agents mirror at {self.agents_skill}",
        )
        canonical_text = self.canonical_skill.read_text(encoding="utf8")
        agents_text = self.agents_skill.read_text(encoding="utf8")
        self.assertEqual(
            canonical_text,
            agents_text,
            ".agents/skills/i-have-adhd/SKILL.md does not match skills/i-have-adhd/SKILL.md",
        )

    def test_antigravity_frontmatter_validity(self):
        content = self.agents_skill.read_text(encoding="utf8")
        self.assertTrue(content.startswith("---"), "Frontmatter opening missing")
        parts = content.split("---", 2)
        self.assertGreaterEqual(len(parts), 3, "Frontmatter not properly delimited")
        frontmatter = parts[1]
        self.assertIn("name: i-have-adhd", frontmatter)
        self.assertIn("description:", frontmatter)

    def test_agents_md_runtime_entry(self):
        content = self.agents_md.read_text(encoding="utf8")
        self.assertIn("Antigravity", content)
        self.assertIn(".agents/skills/i-have-adhd/SKILL.md", content)

    def test_install_md_antigravity_sections(self):
        content = self.install_md.read_text(encoding="utf8")
        marker = "<summary><strong>Antigravity"
        self.assertIn(marker, content)
        section = content.split(marker, 1)[1].split("</details>", 1)[0]
        self.assertIn(".agents/skills/i-have-adhd", section)
        self.assertIn("builtin/skills/i-have-adhd", section)


if __name__ == "__main__":
    unittest.main()
