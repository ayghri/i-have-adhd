import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "generate_rules.mjs"


class GenerateRulesTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.script_dir = Path(self.temp_dir.name) / "scripts"
        self.script_dir.mkdir()
        shutil.copy(GENERATOR, self.script_dir / "generate_rules.mjs")

        self.skill_dir = Path(self.temp_dir.name) / "skills" / "i-have-adhd"
        self.skill_dir.mkdir(parents=True)

    def run_generator(self, skill_content):
        (self.skill_dir / "SKILL.md").write_text(skill_content)
        result = subprocess.run(
            ["node", str(self.script_dir / "generate_rules.mjs")],
            cwd=self.temp_dir.name,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        return (self.skill_dir / "rules.md").read_text()

    def test_strips_frontmatter_with_trailing_whitespace(self):
        rules = self.run_generator("---   \nname: fixture\n--- \t\nFixture body.\n")

        self.assertNotIn("name: fixture", rules)
        self.assertEqual("Fixture body.\n", rules)

    def test_keeps_content_when_frontmatter_is_unclosed(self):
        # An opening --- with no closing delimiter is not frontmatter. Keeping
        # the whole file beats generating a rules.md that promises "the
        # ruleset below" (via the hook banner) followed by nothing.
        rules = self.run_generator(
            "---\nname: fixture\nFixture body, fence never closed.\n"
        )

        self.assertIn("Fixture body, fence never closed.", rules)

    def test_fails_when_stripping_leaves_nothing(self):
        result = subprocess.run(
            ["node", str(self.script_dir / "generate_rules.mjs")],
            cwd=self.temp_dir.name,
            capture_output=True,
            text=True,
        )
        # No SKILL.md at all: readFileSync throws before the emptiness check.
        self.assertNotEqual(0, result.returncode)

        (self.skill_dir / "SKILL.md").write_text("---\nname: fixture\n---\n")
        result = subprocess.run(
            ["node", str(self.script_dir / "generate_rules.mjs")],
            cwd=self.temp_dir.name,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("Stripping frontmatter left no content", result.stderr)


if __name__ == "__main__":
    unittest.main()
