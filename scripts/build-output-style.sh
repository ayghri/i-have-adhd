#!/bin/sh
# Regenerate the Claude Code output style from the skill, the single source of truth.
# The body is copied verbatim from skills/i-have-adhd/SKILL.md; only the frontmatter
# differs. Rerun this after editing SKILL.md, then commit both files.
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
skill="$root/skills/i-have-adhd/SKILL.md"
out="$root/output-styles/i-have-adhd.md"

mkdir -p "$root/output-styles"

{
  cat <<'EOF'
---
name: i-have-adhd
description: 'Shape output for an ADHD reader: action-first, numbered steps, no preamble or closers, state restated each turn.'
keep-coding-instructions: true
---

<!-- GENERATED from skills/i-have-adhd/SKILL.md by scripts/build-output-style.sh — do not edit by hand. -->
EOF
  # Skill body: every line after the frontmatter (i.e. after the second `---`).
  awk 'body { print; next } /^---[[:space:]]*$/ { if (++n == 2) body = 1 }' "$skill"
} > "$out"

echo "wrote $out"
