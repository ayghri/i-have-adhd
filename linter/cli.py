#!/usr/bin/env python3
"""
CLI for the ADHD linter.

Usage:
    python3 linter/cli.py "Your response text"
    cat response.txt | python3 linter/cli.py
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import the linter
sys.path.insert(0, str(Path(__file__).parent.parent))

from linter.adhd_linter import ADHDLinter, format_violations


def main():
    """Run the linter on input text."""
    if len(sys.argv) > 1:
        # Text passed as argument
        text = " ".join(sys.argv[1:])
    else:
        # Read from stdin
        text = sys.stdin.read()

    if not text.strip():
        print("No input provided.")
        return 1

    linter = ADHDLinter(text)
    violations = linter.lint()

    if violations:
        print(format_violations(violations))
        return 1
    else:
        print(format_violations(violations))
        return 0


if __name__ == "__main__":
    sys.exit(main())
