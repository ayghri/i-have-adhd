#!/usr/bin/env python3
"""Project package.json's shared fields into the other harness manifests.

name, version, description, license, homepage, and author used to be
hand-typed separately in up to nine files (package.json, kimi.plugin.json,
plugin.json, .claude-plugin/plugin.json, .claude-plugin/marketplace.json,
.codex-plugin/plugin.json, .agents/plugins/marketplace.json,
gemini-extension.json, qwen-extension.json), so a version bump meant six
edits and nothing caught the ones that got missed.

package.json is now the canonical source. Every other manifest keeps its
own harness-specific fields (interface blocks, capabilities, per-harness
description text, ...) but has its copies of the shared fields rendered
from package.json. Do not hand-edit the mapped fields below: edit
package.json, then run
    python3 scripts/render_manifests.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "package.json"

# (file relative to ROOT, [(dotted path in that file, dotted path in source)])
TARGETS: list[tuple[str, list[tuple[str, str]]]] = [
    (
        "kimi.plugin.json",
        [
            ("name", "name"),
            ("version", "version"),
            ("description", "description"),
            ("license", "license"),
            ("homepage", "homepage"),
        ],
    ),
    (
        "plugin.json",
        [
            ("name", "name"),
        ],
    ),
    (
        ".claude-plugin/plugin.json",
        [
            ("name", "name"),
            ("version", "version"),
            ("author", "author"),
        ],
    ),
    (
        ".claude-plugin/marketplace.json",
        [
            ("name", "name"),
            ("owner.name", "author.name"),
            ("plugins.0.name", "name"),
        ],
    ),
    (
        ".codex-plugin/plugin.json",
        [
            ("name", "name"),
            ("version", "version"),
            ("author", "author"),
            ("homepage", "homepage"),
            ("license", "license"),
            ("repository", "homepage"),
            ("interface.developerName", "author.name"),
            ("interface.websiteURL", "homepage"),
        ],
    ),
    (
        ".agents/plugins/marketplace.json",
        [
            ("name", "name"),
            ("plugins.0.name", "name"),
        ],
    ),
    (
        "gemini-extension.json",
        [
            ("name", "name"),
            ("version", "version"),
        ],
    ),
    (
        "qwen-extension.json",
        [
            ("name", "name"),
            ("version", "version"),
        ],
    ),
]


def _get(data: Any, dotted_path: str) -> Any:
    node = data
    for segment in dotted_path.split("."):
        key: Any = int(segment) if segment.isdigit() else segment
        node = node[key]
    return node


def _set(data: Any, dotted_path: str, value: Any) -> None:
    segments = dotted_path.split(".")
    node = data
    for segment in segments[:-1]:
        key: Any = int(segment) if segment.isdigit() else segment
        node = node[key]
    last: Any = int(segments[-1]) if segments[-1].isdigit() else segments[-1]
    if isinstance(node, dict):
        missing = last not in node
    else:
        missing = last >= len(node)
    if missing:
        raise KeyError(
            f"{dotted_path!r} does not exist yet; add the field by hand once, "
            "then let this script keep it in sync"
        )
    node[last] = value


def render_target(source: dict[str, Any], relative_path: str, mapping: list[tuple[str, str]]) -> str:
    target_path = ROOT / relative_path
    data = json.loads(target_path.read_text(encoding="utf8"))
    for target_field, source_field in mapping:
        _set(data, target_field, _get(source, source_field))
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    source = json.loads(SOURCE_PATH.read_text(encoding="utf8"))
    check = "--check" in sys.argv[1:]
    out_of_sync: list[str] = []

    for relative_path, mapping in TARGETS:
        rendered = render_target(source, relative_path, mapping)
        target_path = ROOT / relative_path

        if check:
            current = target_path.read_text(encoding="utf8")
            if current != rendered:
                out_of_sync.append(relative_path)
            continue

        target_path.write_text(rendered, encoding="utf8")
        print(f"Wrote {relative_path}")

    if check:
        if out_of_sync:
            print(
                "Out of sync with package.json: " + ", ".join(out_of_sync) + "\n"
                "Run: python3 scripts/render_manifests.py",
                file=sys.stderr,
            )
            return 1
        print("All manifests match package.json")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
