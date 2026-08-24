#!/usr/bin/env python3
"""Check that shared-core sections are identical across all family skills.

ADR 0004: `## Persistence`, `## When to break the rules`, and `## Pre-send check`
must be textually identical across skills/<name>/SKILL.md, after normalizing each
skill's own mode token (the condition word in "stop <mode> mode") to `<mode>`.
The reference is the upstream i-have-adhd skill, which stays byte-identical to
upstream.

Also validates frontmatter basics: `name` matches the directory, `description`
present and <= 1024 chars.

Exit 0 when clean; exit 1 with a per-file problem list otherwise.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SHARED_SECTIONS = ["Persistence", "When to break the rules", "Pre-send check"]
REFERENCE_DIR = "i-have-adhd"
MAX_DESCRIPTION = 1024

REPO_ROOT = Path(__file__).resolve().parent.parent


def extract_sections(text: str) -> dict[str, str]:
    """Return {h2 title: section body} for an h2-delimited markdown file."""
    sections: dict[str, str] = {}
    current: str | None = None
    lines: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^## (.+?)\s*$", line)
        if match:
            if current is not None:
                sections[current] = "\n".join(lines).strip()
            current = match.group(1)
            lines = []
        elif current is not None:
            lines.append(line)
    if current is not None:
        sections[current] = "\n".join(lines).strip()
    return sections


def normalize(body: str, mode: str) -> str:
    return body.replace(mode, "<mode>")


def mode_of(skill_dir: Path) -> str:
    return skill_dir.name.removeprefix("i-have-")


def check_description(text: str, skill_dir: Path, problems: list[str]) -> None:
    match = re.search(r"^description:\s*(.+)$", text, re.MULTILINE)
    if not match:
        problems.append(f"{skill_dir.name}: frontmatter `description` missing")
        return
    desc = match.group(1).strip().strip("'\"")
    if len(desc) > MAX_DESCRIPTION:
        problems.append(
            f"{skill_dir.name}: description {len(desc)} chars > {MAX_DESCRIPTION}"
        )


def check_name(text: str, skill_dir: Path, problems: list[str]) -> None:
    match = re.search(r"^name:\s*(.+)$", text, re.MULTILINE)
    if not match or match.group(1).strip() != skill_dir.name:
        problems.append(f"{skill_dir.name}: frontmatter `name` missing or mismatched")


def main() -> int:
    skills_root = REPO_ROOT / "skills"
    skill_dirs = sorted(p for p in skills_root.iterdir() if (p / "SKILL.md").exists())
    if not skill_dirs:
        print("no skills found under skills/")
        return 1

    problems: list[str] = []
    reference_path = skills_root / REFERENCE_DIR / "SKILL.md"
    if not reference_path.exists():
        print(f"reference skill missing: {reference_path}")
        return 1
    reference_sections = extract_sections(reference_path.read_text(encoding="utf-8"))
    for section in SHARED_SECTIONS:
        if section not in reference_sections:
            print(f"reference skill is missing shared section: {section}")
            return 1
    reference = {
        s: normalize(reference_sections[s], mode_of(reference_path.parent))
        for s in SHARED_SECTIONS
    }

    for skill_dir in skill_dirs:
        text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        check_name(text, skill_dir, problems)
        check_description(text, skill_dir, problems)

        sections = extract_sections(text)
        for section in SHARED_SECTIONS:
            if section not in sections:
                problems.append(f"{skill_dir.name}: shared section missing: {section}")
                continue
            got = normalize(sections[section], mode_of(skill_dir))
            want = reference[section]
            if got != want:
                problems.append(
                    f"{skill_dir.name}: shared section drifted: {section}\n"
                    f"--- reference (normalized) ---\n{want}\n"
                    f"--- {skill_dir.name} (normalized) ---\n{got}"
                )

    if problems:
        print(f"shared-core check FAILED ({len(problems)} problem(s)):")
        for p in problems:
            print(f"- {p}")
        return 1
    print(f"shared-core check OK across {len(skill_dirs)} skills")
    return 0


if __name__ == "__main__":
    sys.exit(main())
