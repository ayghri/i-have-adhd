"""Checks that README language links point to existing files."""

import pathlib
import re
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class ReadmeLanguageLinkTest(unittest.TestCase):
    def test_language_links_exist(self):
        readme = (ROOT / "README.md").read_text(encoding="utf8")
        links = re.findall(r'href="(\.github/readme/README\.[^"]+\.md)"', readme)

        self.assertTrue(links, "No localized README links found")
        for link in links:
            with self.subTest(link=link):
                self.assertTrue((ROOT / link).is_file(), f"Missing localized README: {link}")


if __name__ == "__main__":
    unittest.main()