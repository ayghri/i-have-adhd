import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class BuildClaudeMdTest(unittest.TestCase):
    """scripts/build_claude_md.sh shares its frontmatter parser with the
    always-on hooks. These lock the shared behaviour in place so the generator
    cannot silently drift back to a single-pass read (see #103)."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.tree = Path(self.temp_dir.name) / "tree"
        (self.tree / "scripts").mkdir(parents=True)
        (self.tree / "skills" / "i-have-adhd").mkdir(parents=True)
        shutil.copy(ROOT / "scripts" / "build_claude_md.sh", self.tree / "scripts")
        self.skill = self.tree / "skills" / "i-have-adhd" / "SKILL.md"

    def build(self, skill_text):
        self.skill.write_text(skill_text, encoding="utf-8")
        sh = shutil.which("sh")
        if not sh:
            self.skipTest("sh is unavailable")
        return subprocess.run(
            [sh, str(self.tree / "scripts" / "build_claude_md.sh")],
            capture_output=True,
            text=True,
        )

    def test_frontmatter_is_stripped_and_body_h1_dropped(self):
        result = self.build("---\nname: x\n---\n\n# i-have-adhd\n\nRule text.\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("name: x", result.stdout)
        self.assertIn("Rule text.", result.stdout)
        self.assertEqual(result.stdout.count("# i-have-adhd"), 1)

    def test_frontmatter_delimiters_tolerate_trailing_whitespace(self):
        result = self.build("---   \nname: x\n---\t\n\n# i-have-adhd\n\nRule text.\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("name: x", result.stdout)
        self.assertIn("Rule text.", result.stdout)

    def test_content_is_kept_when_frontmatter_is_never_closed(self):
        # A leading `---` with no closing delimiter is a horizontal rule, not
        # frontmatter. A single-pass parser swallows the whole ruleset here.
        result = self.build("---\n\n# i-have-adhd\n\nRule text.\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Rule text.", result.stdout)

    def test_committed_claude_md_matches_the_generator(self):
        generated = subprocess.run(
            [shutil.which("sh") or "sh", str(ROOT / "scripts" / "build_claude_md.sh")],
            capture_output=True,
            text=True,
        )
        self.assertEqual(generated.returncode, 0, generated.stderr)
        committed = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertEqual(
            committed,
            generated.stdout,
            "CLAUDE.md is stale; run: sh scripts/build_claude_md.sh > CLAUDE.md",
        )


if __name__ == "__main__":
    unittest.main()
