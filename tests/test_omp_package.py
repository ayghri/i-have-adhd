import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class OmpPackageTest(unittest.TestCase):
    def setUp(self):
        self.package = json.loads((ROOT / "package.json").read_text(encoding="utf8"))

    def test_omp_and_pi_extension_manifests_are_declared(self):
        extension = ["./extensions/i-have-adhd.ts"]
        self.assertEqual({"extensions": extension}, self.package["omp"])
        self.assertEqual(
            {"extensions": extension, "skills": ["./skills"]},
            self.package["pi"],
        )

    def test_skill_remains_explicitly_invoked(self):
        skill = (ROOT / "skills" / "i-have-adhd" / "SKILL.md").read_text(
            encoding="utf8"
        )
        frontmatter = skill.split("---\n", 2)[1]
        self.assertIn("name: i-have-adhd", frontmatter)
        self.assertIn("disable-model-invocation: true", frontmatter)


if __name__ == "__main__":
    unittest.main()
