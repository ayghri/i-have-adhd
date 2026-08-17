#!/usr/bin/env python3
"""Render skills/i-have-adhd/agents/gemini.toml from the canonical ruleset.

Gemini CLI custom commands have no import mechanism, so the ruleset has to be
inlined into the command's prompt string. That inlining used to be a hand
paraphrase, which drifted from SKILL.md (missing rules, missing overrides,
missing the pre-send check). This script reads rules.md instead - the same
parsed copy of the ruleset the other entry points read - so the two
can only go out of sync if this file isn't re-run.
"""

from __future__ import annotations

import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = ROOT / "skills" / "i-have-adhd" / "rules.md"
GEMINI_TOML_PATH = ROOT / "skills" / "i-have-adhd" / "agents" / "gemini.toml"

# Shown in Gemini CLI's command list; not part of the ruleset, so it is not
# derived from SKILL.md's frontmatter description.
GEMINI_DESCRIPTION = "ADHD-friendly output: action-first, numbered steps, no preamble or closers."

HEADER = """# Gemini CLI custom command for i-have-adhd.
# Install: copy to ~/.gemini/commands/i-have-adhd.toml, then type /i-have-adhd.
# Self-contained so it works as a global command from any directory.
#
# Generated from skills/i-have-adhd/rules.md by scripts/render_gemini_command.py.
# Do not hand-edit the prompt below: edit SKILL.md, run
#   node scripts/generate_rules.mjs
# then
#   python3 scripts/render_gemini_command.py
"""


def ruleset_body() -> str:
    body = RULES_PATH.read_text(encoding="utf8").strip("\n")
    if "'''" in body:
        raise ValueError(f"{RULES_PATH} contains a TOML-breaking ''' sequence")
    return body


def render() -> str:
    prompt = f"{ruleset_body()}\n\n{{{{args}}}}"
    rendered = "\n".join(
        [
            HEADER,
            f'description = "{GEMINI_DESCRIPTION}"',
            "",
            # A literal (single-quoted) multi-line string: TOML processes
            # no escapes inside one, so a backslash in the ruleset survives
            # verbatim. A basic ("""-quoted) string would read a \\t in
            # SKILL.md as a tab character.
            "prompt = '''",
            prompt,
            "'''",
            "",
        ]
    )
    tomllib.loads(rendered)  # fail loudly if the ruleset broke TOML syntax
    return rendered


def main() -> int:
    rendered = render()

    if "--check" in sys.argv[1:]:
        current = (
            GEMINI_TOML_PATH.read_text(encoding="utf8")
            if GEMINI_TOML_PATH.exists()
            else None
        )
        if current != rendered:
            print(
                f"{GEMINI_TOML_PATH} is out of sync with {RULES_PATH}.\n"
                "Run: python3 scripts/render_gemini_command.py",
                file=sys.stderr,
            )
            return 1
        print("gemini.toml matches rules.md")
        return 0

    GEMINI_TOML_PATH.write_text(rendered, encoding="utf8")
    print(f"Wrote {GEMINI_TOML_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
