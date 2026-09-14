#!/usr/bin/env python3
"""
ADHD Response Style Linter

Detects violations of the 10 ADHD-friendly response rules.
Rules documented in skills/i-have-adhd/SKILL.md
"""

import re
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Violation:
    """Represents a single rule violation."""
    rule: int
    rule_name: str
    line_number: int
    line_content: str
    message: str
    severity: str  # "error" or "warning"


class ADHDLinter:
    """Lints responses for adherence to ADHD-friendly output rules."""

    # Rule 10: Forbidden openers
    FORBIDDEN_OPENERS = [
        "great question",
        "let me ",
        "i'll ",
        "sure!",
        "looking at your",
        "to answer your question",
        "absolutely",
        "certainly",
        "of course",
    ]

    # Rule 10: Forbidden closers
    FORBIDDEN_CLOSERS = [
        "let me know if you need anything else",
        "hope this helps",
        "happy to clarify",
        "feel free to ask",
        "feel free to reach out",
        "let me know if you have any questions",
        "anything else",
        "let me know if this helps",
    ]

    # Rule 8: Forbidden error openers
    FORBIDDEN_ERROR_OPENERS = [
        "uh oh",
        "oh no",
        "there seems to be",
        "it seems like",
        "it looks like there",
        "appears to be a problem",
    ]

    # Rule 6: Vague time estimates
    VAGUE_TIME_ESTIMATES = [
        r"a bit",
        r"a while",
        r"some time",
        r"a few moments",
        r"shortly",
        r"soon",
        r"quite a bit",
        r"a couple of minutes",  # imprecise
    ]

    def __init__(self, text: str):
        self.text = text
        self.lines = text.split("\n")
        self.violations: List[Violation] = []

    def lint(self) -> List[Violation]:
        """Run all lint checks and return violations."""
        self._check_rule_1_lead_with_action()
        self._check_rule_2_numbered_steps()
        self._check_rule_3_concrete_next_action()
        self._check_rule_6_specific_time_estimates()
        self._check_rule_8_error_tone()
        self._check_rule_10_preamble_recap_closers()
        return self.violations

    def _check_rule_1_lead_with_action(self) -> None:
        """Rule 1: Lead with the next action."""
        if not self.lines:
            return

        first_line = self.lines[0].strip().lower()

        # Check for forbidden openers
        for opener in self.FORBIDDEN_OPENERS:
            if first_line.startswith(opener):
                self.violations.append(
                    Violation(
                        rule=1,
                        rule_name="Lead with the next action",
                        line_number=1,
                        line_content=self.lines[0],
                        message=f'First line starts with forbidden opener: "{opener}". Start with an action instead.',
                        severity="error",
                    )
                )
                return

        # Check if first line is context/explanation instead of action
        context_indicators = [
            "your",
            "the",
            "this",
            "in your",
            "looking at",
            "examining",
        ]
        
        # If starts with context instead of imperative verb or command
        if first_line and not self._is_action_line(first_line):
            self.violations.append(
                Violation(
                    rule=1,
                    rule_name="Lead with the next action",
                    line_number=1,
                    line_content=self.lines[0],
                    message="First line should lead with an action (command, path, or code snippet), not context.",
                    severity="warning",
                )
            )

    def _is_action_line(self, line: str) -> bool:
        """Check if a line starts with an action."""
        action_verbs = [
            "run",
            "open",
            "edit",
            "replace",
            "create",
            "delete",
            "fix",
            "add",
            "remove",
            "install",
            "check",
            "verify",
            "paste",
            "copy",
            "clone",
            "commit",
            "push",
            "pull",
            "merge",
            "`",  # code block
            "$",  # command
        ]
        
        return any(line.startswith(verb) for verb in action_verbs)

    def _check_rule_2_numbered_steps(self) -> None:
        """Rule 2: Number multi-step tasks."""
        step_pattern = re.compile(r"^\s*\d+\.\s+")
        
        # Find if there are multiple action lines without numbering
        action_count = 0
        first_action_line = None
        
        for i, line in enumerate(self.lines):
            stripped = line.strip()
            if self._is_action_line(stripped) and not step_pattern.match(line):
                if action_count == 0:
                    first_action_line = i + 1
                action_count += 1
        
        # If 3+ actions without numbering, flag it
        if action_count >= 3:
            self.violations.append(
                Violation(
                    rule=2,
                    rule_name="Number multi-step tasks",
                    line_number=first_action_line or 1,
                    line_content=self.lines[first_action_line - 1] if first_action_line else "",
                    message=f"Found {action_count} actions without numbering. Use numbered list for multi-step work.",
                    severity="warning",
                )
            )

    def _check_rule_3_concrete_next_action(self) -> None:
        """Rule 3: End with one concrete next action."""
        if len(self.lines) < 2:
            return

        last_non_empty = ""
        last_line_idx = 0
        
        for i in range(len(self.lines) - 1, -1, -1):
            if self.lines[i].strip():
                last_non_empty = self.lines[i].strip().lower()
                last_line_idx = i + 1
                break

        if not last_non_empty:
            return

        # Check for bad endings
        bad_endings = [
            "let me know if you need anything else",
            "hope this helps",
            "anything else?",
            "any questions?",
            "feel free to ask",
            "let me know",
            "happy to help",
        ]

        for ending in bad_endings:
            if ending in last_non_empty:
                self.violations.append(
                    Violation(
                        rule=3,
                        rule_name="End with one concrete next action",
                        line_number=last_line_idx,
                        line_content=self.lines[last_line_idx - 1],
                        message=f'Remove closing pleasantry: "{ending}". End with a concrete action instead.',
                        severity="error",
                    )
                )
                return

        # Check if last line is a concrete action
        if not self._is_action_line(last_non_empty):
            self.violations.append(
                Violation(
                    rule=3,
                    rule_name="End with one concrete next action",
                    line_number=last_line_idx,
                    line_content=self.lines[last_line_idx - 1],
                    message="Last line should be a concrete next action (doable in under 2 minutes).",
                    severity="warning",
                )
            )

    def _check_rule_6_specific_time_estimates(self) -> None:
        """Rule 6: Give specific time estimates."""
        for i, line in enumerate(self.lines):
            line_lower = line.lower()
            
            for vague in self.VAGUE_TIME_ESTIMATES:
                if re.search(vague, line_lower):
                    # Check if this is followed by a specific estimate
                    if not re.search(r"\d+\s*(minute|hour|second|day)", line_lower):
                        self.violations.append(
                            Violation(
                                rule=6,
                                rule_name="Give specific time estimates",
                                line_number=i + 1,
                                line_content=line,
                                message=f'Vague time estimate: "{vague}". Use concrete units (e.g., "15 minutes").',
                                severity="warning",
                            )
                        )
                        break

    def _check_rule_8_error_tone(self) -> None:
        """Rule 8: Matter-of-fact tone for errors."""
        for i, line in enumerate(self.lines):
            line_lower = line.lower()
            
            for opener in self.FORBIDDEN_ERROR_OPENERS:
                if re.search(opener, line_lower):
                    self.violations.append(
                        Violation(
                            rule=8,
                            rule_name="Matter-of-fact tone for errors",
                            line_number=i + 1,
                            line_content=line,
                            message=f'Avoid dramatic error language: "{opener}". State cause and fix directly.',
                            severity="error",
                        )
                    )
                    break

    def _check_rule_10_preamble_recap_closers(self) -> None:
        """Rule 10: No preamble, no recap, no closing pleasantries."""
        if not self.lines:
            return

        # Check first line for forbidden openers (already caught by rule 1)
        # but catch ones we might have missed
        first_line = self.lines[0].strip().lower()
        
        more_forbidden_openers = [
            "this will",
            "what you need to do is",
            "here's what",
            "the answer is",
        ]
        
        for opener in more_forbidden_openers:
            if first_line.startswith(opener):
                self.violations.append(
                    Violation(
                        rule=10,
                        rule_name="No preamble, no recap, no closing pleasantries",
                        line_number=1,
                        line_content=self.lines[0],
                        message=f'Preamble detected: "{opener}". Start with the answer directly.',
                        severity="error",
                    )
                )

        # Check for recaps like "I've now done X, Y, and Z"
        for i, line in enumerate(self.lines):
            line_lower = line.lower()
            if re.search(r"i'?ve\s+(now\s+)?done", line_lower) or re.search(r"i'?ve\s+made", line_lower):
                self.violations.append(
                    Violation(
                        rule=10,
                        rule_name="No preamble, no recap, no closing pleasantries",
                        line_number=i + 1,
                        line_content=line,
                        message='Avoid recaps like "I\'ve done X". State what works directly instead.',
                        severity="warning",
                    )
                )

        # Check last line for forbidden closers (already caught by rule 3 mostly)
        if len(self.lines) > 1:
            last_line = self.lines[-1].strip().lower()
            for closer in self.FORBIDDEN_CLOSERS:
                if closer in last_line:
                    self.violations.append(
                        Violation(
                            rule=10,
                            rule_name="No preamble, no recap, no closing pleasantries",
                            line_number=len(self.lines),
                            line_content=self.lines[-1],
                            message=f'Remove closing pleasantry: "{closer}".',
                            severity="error",
                        )
                    )


def format_violations(violations: List[Violation]) -> str:
    """Format violations for console output."""
    if not violations:
        return "✓ No violations found."

    output = [f"\n{len(violations)} violation(s) found:\n"]
    
    for v in violations:
        severity_mark = "❌" if v.severity == "error" else "⚠️"
        output.append(
            f"{severity_mark} Line {v.line_number} (Rule {v.rule}): {v.rule_name}\n"
            f"   {v.message}\n"
            f"   {v.line_content[:80]}\n"
        )
    
    return "".join(output)
