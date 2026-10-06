"""ADHD Linter - Checks response text for ADHD-friendly output rule compliance."""

from linter.adhd_linter import ADHDLinter, Violation, format_violations

__all__ = ["ADHDLinter", "Violation", "format_violations"]
__version__ = "0.1.0"
