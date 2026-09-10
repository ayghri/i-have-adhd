#!/usr/bin/env python3
"""
Unit tests for ADHD Linter

Tests that the linter correctly detects violations of each rule.
"""

import unittest
from linter.adhd_linter import ADHDLinter, Violation


class TestRule1LeadWithAction(unittest.TestCase):
    """Test Rule 1: Lead with the next action."""

    def test_good_lead_with_command(self):
        """Should pass when leading with a command."""
        text = "Run `npm install`.\n\nThen edit the file."
        linter = ADHDLinter(text)
        violations = linter.lint()
        rule_1_violations = [v for v in violations if v.rule == 1]
        self.assertEqual(len(rule_1_violations), 0)

    def test_bad_lead_with_preamble(self):
        """Should fail when starting with 'Great question'."""
        text = "Great question! Let me think about this..."
        linter = ADHDLinter(text)
        violations = linter.lint()
        rule_1_violations = [v for v in violations if v.rule == 1]
        self.assertGreater(len(rule_1_violations), 0)
        self.assertIn("forbidden opener", rule_1_violations[0].message.lower())

    def test_bad_lead_with_let_me(self):
        """Should fail when starting with 'Let me'."""
        text = "Let me walk you through this step by step."
        linter = ADHDLinter(text)
        violations = linter.lint()
        rule_1_violations = [v for v in violations if v.rule == 1]
        self.assertGreater(len(rule_1_violations), 0)

    def test_good_lead_with_path(self):
        """Should pass when leading with a file path."""
        text = "Open `src/auth.ts:42`."
        linter = ADHDLinter(text)
        violations = linter.lint()
        rule_1_violations = [v for v in violations if v.rule == 1]
        self.assertEqual(len(rule_1_violations), 0)


class TestRule2NumberedSteps(unittest.TestCase):
    """Test Rule 2: Number multi-step tasks."""

    def test_good_numbered_steps(self):
        """Should pass when steps are numbered."""
        text = """1. Open the file
2. Find the function
3. Replace it
4. Run tests"""
        linter = ADHDLinter(text)
        violations = linter.lint()
        rule_2_violations = [v for v in violations if v.rule == 2]
        self.assertEqual(len(rule_2_violations), 0)

    def test_bad_unnumbered_multiple_actions(self):
        """Should fail when 3+ actions lack numbering."""
        text = """Open the file
Edit line 42
Replace the function
Run npm test
Check the logs"""
        linter = ADHDLinter(text)
        violations = linter.lint()
        rule_2_violations = [v for v in violations if v.rule == 2]
        self.assertGreater(len(rule_2_violations), 0)

    def test_good_single_action(self):
        """Should pass when there's only one action."""
        text = "Run `npm install`."
        linter = ADHDLinter(text)
        violations = linter.lint()
        rule_2_violations = [v for v in violations if v.rule == 2]
        self.assertEqual(len(rule_2_violations), 0)


class TestRule3ConcreteNextAction(unittest.TestCase):
    """Test Rule 3: End with one concrete next action."""

    def test_good_ends_with_action(self):
        """Should pass when ending with a concrete action."""
        text = "The fix is applied.\n\nNext: run `npm test` and paste the first failing line."
        linter = ADHDLinter(text)
        violations = linter.lint()
        rule_3_violations = [v for v in violations if v.rule == 3]
        self.assertEqual(len(rule_3_violations), 0)

    def test_bad_ends_with_closer(self):
        """Should fail when ending with 'Hope this helps'."""
        text = "Here's your answer.\n\nHope this helps!"
        linter = ADHDLinter(text)
        violations = linter.lint()
        rule_3_violations = [v for v in violations if v.rule == 3]
        self.assertGreater(len(rule_3_violations), 0)
        self.assertIn("closing pleasantry", rule_3_violations[0].message.lower())

    def test_bad_ends_with_question(self):
        """Should fail when ending with 'Let me know if you need anything else'."""
        text = "Done.\n\nLet me know if you need anything else."
        linter = ADHDLinter(text)
        violations = linter.lint()
        rule_3_violations = [v for v in violations if v.rule == 3]
        self.assertGreater(len(rule_3_violations), 0)


class TestRule6SpecificTimeEstimates(unittest.TestCase):
    """Test Rule 6: Give specific time estimates."""

    def test_good_specific_estimate(self):
        """Should pass when time is specific."""
        text = "This will take about 15 minutes."
        linter = ADHDLinter(text)
        violations = linter.lint()
        rule_6_violations = [v for v in violations if v.rule == 6]
        self.assertEqual(len(rule_6_violations), 0)

    def test_bad_vague_estimate_a_bit(self):
        """Should fail when using 'a bit'."""
        text = "This will take a bit of work."
        linter = ADHDLinter(text)
        violations = linter.lint()
        rule_6_violations = [v for v in violations if v.rule == 6]
        self.assertGreater(len(rule_6_violations), 0)
        self.assertIn("vague", rule_6_violations[0].message.lower())

    def test_bad_vague_estimate_a_while(self):
        """Should fail when using 'a while'."""
        text = "This will take a while."
        linter = ADHDLinter(text)
        violations = linter.lint()
        rule_6_violations = [v for v in violations if v.rule == 6]
        self.assertGreater(len(rule_6_violations), 0)

    def test_good_range_estimate(self):
        """Should pass with specific range."""
        text = "About 10-15 minutes if tests pass, an hour if they don't."
        linter = ADHDLinter(text)
        violations = linter.lint()
        rule_6_violations = [v for v in violations if v.rule == 6]
        self.assertEqual(len(rule_6_violations), 0)


class TestRule8ErrorTone(unittest.TestCase):
    """Test Rule 8: Matter-of-fact tone for errors."""

    def test_good_error_description(self):
        """Should pass when stating error matter-of-factly."""
        text = "Test fails at auth.spec.ts:42: expected 200, got 401. Cause: missing header."
        linter = ADHDLinter(text)
        violations = linter.lint()
        rule_8_violations = [v for v in violations if v.rule == 8]
        self.assertEqual(len(rule_8_violations), 0)

    def test_bad_error_with_uh_oh(self):
        """Should fail when using 'Uh oh'."""
        text = "Uh oh, something went wrong."
        linter = ADHDLinter(text)
        violations = linter.lint()
        rule_8_violations = [v for v in violations if v.rule == 8]
        self.assertGreater(len(rule_8_violations), 0)
        self.assertIn("dramatic", rule_8_violations[0].message.lower())

    def test_bad_error_with_oh_no(self):
        """Should fail when using 'Oh no'."""
        text = "Oh no, the test failed."
        linter = ADHDLinter(text)
        violations = linter.lint()
        rule_8_violations = [v for v in violations if v.rule == 8]
        self.assertGreater(len(rule_8_violations), 0)

    def test_bad_error_with_there_seems(self):
        """Should fail when using 'There seems to be'."""
        text = "There seems to be a problem with your code."
        linter = ADHDLinter(text)
        violations = linter.lint()
        rule_8_violations = [v for v in violations if v.rule == 8]
        self.assertGreater(len(rule_8_violations), 0)


class TestRule10PreambleRecapClosers(unittest.TestCase):
    """Test Rule 10: No preamble, no recap, no closing pleasantries."""

    def test_good_direct_start(self):
        """Should pass when starting directly."""
        text = "Run `npm install`."
        linter = ADHDLinter(text)
        violations = linter.lint()
        rule_10_violations = [v for v in violations if v.rule == 10]
        self.assertEqual(len(rule_10_violations), 0)

    def test_bad_preamble_what_you_need(self):
        """Should fail with 'what you need to do is'."""
        text = "What you need to do is open the file and edit it."
        linter = ADHDLinter(text)
        violations = linter.lint()
        rule_10_violations = [v for v in violations if v.rule == 10]
        self.assertGreater(len(rule_10_violations), 0)

    def test_bad_recap_ive_done(self):
        """Should fail with 'I've done X, Y, and Z'."""
        text = "I've now done the schema update, backfilled the column, and deployed."
        linter = ADHDLinter(text)
        violations = linter.lint()
        rule_10_violations = [v for v in violations if v.rule == 10]
        self.assertGreater(len(rule_10_violations), 0)
        self.assertIn("recap", rule_10_violations[0].message.lower())

    def test_bad_closer(self):
        """Should fail with forbidden closer."""
        text = "Here's the fix.\n\nLet me know if you need anything else."
        linter = ADHDLinter(text)
        violations = linter.lint()
        rule_10_violations = [v for v in violations if v.rule == 10]
        self.assertGreater(len(rule_10_violations), 0)


class TestIntegration(unittest.TestCase):
    """Integration tests with realistic responses."""

    def test_good_response(self):
        """Should find no violations in a well-formed response."""
        text = """Run `npm install jsonwebtoken@latest`.

1. Open `src/auth.ts`
2. Replace `verifyToken` (lines 42–58) with the snippet below
3. Run `npm test -- auth.spec.ts`

Next: paste the first failing line if any test fails."""
        linter = ADHDLinter(text)
        violations = linter.lint()
        self.assertEqual(len(violations), 0)

    def test_bad_response_multiple_violations(self):
        """Should catch multiple violations in a poor response."""
        text = """Great question! Let me think about this.

Your auth flow has several moving pieces. Here's what you need to do:

1. Open the file
2. Find the function
3. Replace it
4. Run the tests

This will take a bit of work. 

I hope this helps!"""
        linter = ADHDLinter(text)
        violations = linter.lint()
        
        # Should have violations for: preamble, vague time, closer
        self.assertGreater(len(violations), 0)
        
        # Check we caught different rules
        rules_caught = set(v.rule for v in violations)
        self.assertIn(1, rules_caught)  # Preamble
        self.assertIn(6, rules_caught)  # Vague time
        self.assertIn(10, rules_caught)  # Closer or recap


if __name__ == "__main__":
    unittest.main()
