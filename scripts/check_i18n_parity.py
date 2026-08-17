#!/usr/bin/env python3
"""Check that translated INSTALL.md / README.md files stay in structural sync
with their English source.

INSTALL.md and README.md are duplicated by hand into five languages each
(.github/install/INSTALL.{ja,ko,pt-BR,vi,zh-CN}.md and
.github/readme/README.{ja,ko,pt-BR,vi,zh-CN}.md). Prose is meant to be
translated; commands are not. This script does not try to translate or
restructure anything -- it only asserts that a translated file has the same
shape as the English source:

  1. Same sequence of structure markers: heading levels and the <summary>
     openers that delimit each harness's <details> section (heading and
     summary *text* is expected to differ, so only the shape is compared).
     Without the summary markers a whole harness section could go missing
     from a translation unnoticed, since those sections use <summary>
     rather than headings.
  2. Same sequence of fenced code blocks, by info-string language.
  3. For non-prose code blocks (bash/sh/text/json/...), the same command
     content line-for-line, ignoring inline "# ..." comments (those may be
     translated) and ignoring language differences inside a
     ```markdown ... ``` block (that fence is prose meant for translation,
     e.g. the "Output style" ruleset snippet).

Run directly to check every known pair; exits non-zero and prints every
mismatch found if any pair has drifted.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Pair:
    """An English source and the directory of translations to hold to its shape."""

    english: Path
    translated_dir: Path
    stem: str

    def translations(self) -> list[Path]:
        return sorted(self.translated_dir.glob(f"{self.stem}.*.md"))


PAIRS = [
    Pair(ROOT / "INSTALL.md", ROOT / ".github" / "install", "INSTALL"),
    Pair(ROOT / "README.md", ROOT / ".github" / "readme", "README"),
]

# Fenced code blocks in this language are prose (e.g. the translated
# "Output style" ruleset snippet), not commands -- skip content comparison.
PROSE_LANGS = {"markdown"}

HEADING_RE = re.compile(r"^(#{1,6})\s+\S")
# CommonMark allows a fence to be indented by up to three spaces, e.g. inside
# a list item. Anchoring at column 0 silently skipped those.
FENCE_RE = re.compile(r"^ {0,3}```(\S*)\s*$")
# Each harness gets a <details> block whose <summary> is its only title; these
# sections carry no heading, so they are invisible to HEADING_RE.
SUMMARY_RE = re.compile(r"^\s*<summary>")


@dataclass
class CodeBlock:
    line: int
    lang: str
    lines: list[str]


def parse(path: Path) -> tuple[list[str], list[CodeBlock]]:
    """Return (structure markers outside code fences, code blocks in order).

    A marker is ``h<level>`` for a Markdown heading or ``section`` for a
    <summary> opener. Raises ValueError on an unterminated fence, which would
    otherwise swallow the rest of the file without a word.
    """
    structure: list[str] = []
    blocks: list[CodeBlock] = []
    current: CodeBlock | None = None

    for lineno, raw in enumerate(path.read_text(encoding="utf8").splitlines(), 1):
        fence = FENCE_RE.match(raw)
        if fence:
            if current is None:
                current = CodeBlock(line=lineno, lang=fence.group(1), lines=[])
            else:
                blocks.append(current)
                current = None
            continue
        if current is not None:
            current.lines.append(raw)
            continue
        heading = HEADING_RE.match(raw)
        if heading:
            structure.append(f"h{len(heading.group(1))}")
        elif SUMMARY_RE.match(raw):
            structure.append("section")

    if current is not None:
        raise ValueError(
            f"{path}:{current.line}: code fence is never closed"
        )

    return structure, blocks


def strip_comment(line: str) -> str:
    """Drop a trailing '# ...' comment (may legitimately be translated)."""
    out = []
    in_backtick = False
    for ch in line:
        if ch == "`":
            in_backtick = not in_backtick
        if ch == "#" and not in_backtick:
            break
        out.append(ch)
    return "".join(out).rstrip()


def _first_divergence(
    en_path: Path,
    en_structure: list[str],
    other_path: Path,
    other_structure: list[str],
) -> str:
    """Describe the first marker that differs, so the whole list need not be read."""
    for i, (en_marker, other_marker) in enumerate(zip(en_structure, other_structure)):
        if en_marker != other_marker:
            return (
                f"marker #{i + 1} is {en_marker!r} in {en_path.name} but "
                f"{other_marker!r} in {other_path.name}"
            )

    shared = min(len(en_structure), len(other_structure))
    longer, longer_path = (
        (en_structure, en_path)
        if len(en_structure) > len(other_structure)
        else (other_structure, other_path)
    )
    return (
        f"the first {shared} markers agree; {longer_path.name} then has an "
        f"extra {longer[shared]!r}"
    )


def compare(en_path: Path, other_path: Path) -> list[str]:
    errors: list[str] = []
    en_structure, en_blocks = parse(en_path)
    other_structure, other_blocks = parse(other_path)

    if en_structure != other_structure:
        errors.append(
            f"structure differs: {en_path.name} has {len(en_structure)} markers "
            f"(headings + <details> sections), {other_path.name} has "
            f"{len(other_structure)}. First divergence: "
            + _first_divergence(en_path, en_structure, other_path, other_structure)
        )

    if len(en_blocks) != len(other_blocks):
        errors.append(
            f"code block count differs: {en_path.name} has {len(en_blocks)} "
            f"fenced blocks, {other_path.name} has {len(other_blocks)}"
        )

    for i, (en_block, other_block) in enumerate(zip(en_blocks, other_blocks)):
        if en_block.lang != other_block.lang:
            errors.append(
                f"code block #{i + 1} language differs: "
                f"{en_path.name}:{en_block.line} is `{en_block.lang}`, "
                f"{other_path.name}:{other_block.line} is `{other_block.lang}`"
            )
            continue
        if en_block.lang in PROSE_LANGS:
            continue
        if len(en_block.lines) != len(other_block.lines):
            errors.append(
                f"code block #{i + 1} ({en_block.lang}) line count differs: "
                f"{en_path.name}:{en_block.line} has {len(en_block.lines)} lines, "
                f"{other_path.name}:{other_block.line} has {len(other_block.lines)}"
            )
            continue
        for j, (en_line, other_line) in enumerate(zip(en_block.lines, other_block.lines)):
            if strip_comment(en_line) != strip_comment(other_line):
                errors.append(
                    f"code block #{i + 1} ({en_block.lang}) line {j + 1} differs "
                    f"(ignoring trailing comments):\n"
                    f"    {en_path.name}:{en_block.line + j + 1}: {en_line!r}\n"
                    f"    {other_path.name}:{other_block.line + j + 1}: {other_line!r}"
                )

    return errors


def main() -> int:
    all_errors: list[str] = []

    for pair in PAIRS:
        if not pair.english.exists():
            all_errors.append(f"missing source file: {pair.english}")
            continue
        translated_files = pair.translations()
        if not translated_files:
            all_errors.append(
                f"no translated files found under {pair.translated_dir}"
            )
            continue
        for other_path in translated_files:
            try:
                errors = compare(pair.english, other_path)
            except ValueError as error:
                errors = [str(error)]
            if errors:
                all_errors.append(
                    f"--- {other_path.relative_to(ROOT)} vs "
                    f"{pair.english.relative_to(ROOT)} ---"
                )
                all_errors.extend(errors)

    if all_errors:
        print("i18n parity check failed:\n", file=sys.stderr)
        print("\n".join(all_errors), file=sys.stderr)
        print(
            "\nStructure (headings and <details> sections) and code blocks must "
            "match the English source (prose and comments may be translated; "
            "commands may not).",
            file=sys.stderr,
        )
        return 1

    print("INSTALL.md and README.md translations match the English source structure.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
