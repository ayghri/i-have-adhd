"""Structural checks for the rule set and every copy of it.

These tests are offline and make no model calls. They catch drift between the
canonical skill and the runtime copies (Cursor, Gemini, install snippets,
READMEs) and guard rules 1 to 10 against accidental renames.
"""

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "i-have-adhd" / "SKILL.md"
MIRROR = ROOT / ".cursor" / "skills" / "i-have-adhd" / "SKILL.md"

ORIGINAL_RULES = [
    "Lead with the next action",
    "Number multi-step tasks",
    "End with one concrete next action",
    "Suppress tangents",
    "Restate state every turn",
    "Give specific time estimates",
    "Make completed work visible",
    "Matter-of-fact tone for errors",
    "Cap lists to 5 items",
    "No preamble, no recap, no closing pleasantries",
]
NEW_RULES = [
    "Park open threads in one line",
    "Point back to the action, not to more analysis",
    "Read messages as written",
    "Anchor deadlines to dates",
]
NEW_RULE_CASES = {
    "topic-switch-parking",
    "pending-action",
    "typo-reading",
    "deadline-anchor",
}


def read(path):
    return path.read_text(encoding="utf8")


def rule_headings(text):
    return re.findall(r"^### (\d+)\. (.+)$", text, re.M)


def numbered_items(text):
    return [int(n) for n in re.findall(r"^(\d+)\. ", text, re.M)]


def section(text, start, end):
    return text.split(start, 1)[1].split(end, 1)[0]


class CanonicalSkillTest(unittest.TestCase):
    def setUp(self):
        self.skill = read(SKILL)
        self.rules = section(self.skill, "## Rules\n", "## When to break the rules")

    def test_rules_are_numbered_contiguously(self):
        numbers = [int(n) for n, _ in rule_headings(self.rules)]
        self.assertEqual(list(range(1, len(numbers) + 1)), numbers)

    def test_original_rules_keep_their_numbers_and_titles(self):
        titles = [t for _, t in rule_headings(self.rules)]
        self.assertEqual(ORIGINAL_RULES, titles[: len(ORIGINAL_RULES)])

    def test_new_rules_follow_the_original_ten(self):
        titles = [t for _, t in rule_headings(self.rules)]
        self.assertEqual(NEW_RULES, titles[len(ORIGINAL_RULES):])

    def test_every_new_rule_has_a_bad_and_a_good_example(self):
        blocks = re.split(r"^### \d+\. ", self.rules, flags=re.M)[1:]
        for block in blocks[len(ORIGINAL_RULES):]:
            title = block.splitlines()[0]
            with self.subTest(rule=title):
                self.assertRegex(block, r"(?m)^Bad: ")
                self.assertRegex(block, r"(?m)^Good: ")

    def test_trailing_sections_are_still_present_and_ordered(self):
        order = [
            self.skill.index("## Persistence"),
            self.skill.index("## Rules"),
            self.skill.index("## When to break the rules"),
            self.skill.index("## Pre-send check"),
        ]
        self.assertEqual(sorted(order), order)

    def test_cursor_mirror_is_identical(self):
        self.assertEqual(self.skill, read(MIRROR))


class RuntimeCopiesTest(unittest.TestCase):
    def setUp(self):
        self.count = len(rule_headings(section(
            read(SKILL), "## Rules\n", "## When to break the rules"
        )))

    def test_gemini_command_lists_every_rule(self):
        toml = read(ROOT / "skills" / "i-have-adhd" / "agents" / "gemini.toml")
        prompt = section(toml, 'prompt = """', '"""')
        self.assertEqual(list(range(1, self.count + 1)), numbered_items(prompt))

    def test_every_install_snippet_lists_every_rule(self):
        for path in [ROOT / "INSTALL.md", *sorted((ROOT / ".github" / "install").glob("INSTALL.*.md"))]:
            for i, block in enumerate(read(path).split("## Output style")[1:]):
                snippet = block.split("```", 1)[0]
                with self.subTest(file=path.name, snippet=i + 1):
                    self.assertEqual(list(range(1, self.count + 1)), numbered_items(snippet))

    def test_agents_guide_states_the_rule_count(self):
        self.assertIn(f"the {self.count} ADHD-friendly response rules", read(ROOT / "AGENTS.md"))


class ReadmeTest(unittest.TestCase):
    def setUp(self):
        self.count = len(rule_headings(section(
            read(SKILL), "## Rules\n", "## When to break the rules"
        )))

    def test_english_readme_count_and_list_match_the_skill(self):
        readme = read(ROOT / "README.md")
        self.assertIn(f"{self.count} rules.", readme)
        rules = section(readme, "## The rules", "## Tune it")
        self.assertEqual(list(range(1, self.count + 1)), numbered_items(rules))

    def test_translated_readmes_list_every_rule(self):
        for path in sorted((ROOT / ".github" / "readme").glob("README.*.md")):
            with self.subTest(file=path.name):
                self.assertEqual(self.count, max(numbered_items(read(path))))


class NewRuleEvalCasesTest(unittest.TestCase):
    def test_each_new_rule_has_an_eval_case(self):
        lines = read(ROOT / "evals" / "cases.jsonl").splitlines()
        cases = {c["id"]: c for c in map(json.loads, filter(None, lines))}
        for case_id in sorted(NEW_RULE_CASES):
            with self.subTest(case=case_id):
                self.assertIn(case_id, cases)
                self.assertGreaterEqual(len(cases[case_id]["criteria"]), 2)


if __name__ == "__main__":
    unittest.main()
