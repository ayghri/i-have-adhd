# ADHD Linter

Checks response text for adherence to the 10 ADHD-friendly output rules.

## Installation

```bash
# No external dependencies required beyond Python 3.10+
python3 -m pip install -e .
```

## Usage

### CLI

```bash
python3 linter/cli.py "Your response text here"
```

Or read from a file:

```bash
python3 linter/cli.py < response.txt
```

### Python

```python
from linter.adhd_linter import ADHDLinter

text = """Run npm install.

1. Open src/auth.ts
2. Replace the function
3. Run tests

Next: paste the first failing line."""

linter = ADHDLinter(text)
violations = linter.lint()

for v in violations:
    print(f"Line {v.line_number}: {v.message}")
```

## What it checks

- **Rule 1**: First line leads with an action
- **Rule 2**: Multi-step tasks are numbered
- **Rule 3**: Ends with a concrete next action
- **Rule 6**: Time estimates are specific (not "a bit", "soon", etc)
- **Rule 8**: Error messages are matter-of-fact (no "Uh oh", "Oh no")
- **Rule 10**: No preamble, no recap, no closing pleasantries

## Violations

Each violation includes:
- Rule number and name
- Line number
- The violating text
- Specific message with guidance

Severity is either `error` (likely wrong) or `warning` (style issue).

## Testing

```bash
python3 -m unittest discover -s tests -v
```

## How to use in CI

The workflow `.github/workflows/lint-adhd.yml` runs automatically on:
- PR creation and updates
- Review comments on PRs

It posts warnings and notices without blocking the PR.
