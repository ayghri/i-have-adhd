#!/usr/bin/env sh
# Generates the root CLAUDE.md from the canonical skills/i-have-adhd/SKILL.md
# and prints it to stdout.
#
#   sh scripts/build_claude_md.sh > CLAUDE.md
#
# CLAUDE.md inlines the full ruleset rather than importing it with @, so the
# file is portable: copy it into any project root or into ~/.claude/CLAUDE.md
# and the rules apply without installing the plugin. That portability is what
# makes it a generated file -- .github/workflows/claude-md-sync.yml fails the
# build if the committed copy drifts from SKILL.md.
#
# Pure POSIX sh and awk, no Node and no Python, matching hooks/always-on.sh.

set -eu

script_dir=$(dirname -- "$0")
skill_path="$script_dir/../skills/i-have-adhd/SKILL.md"

if [ ! -f "$skill_path" ]; then
  echo "build_claude_md.sh: cannot read $skill_path" >&2
  exit 1
fi

cat <<'HEADER'
# i-have-adhd

Shape every response for a reader with ADHD. Follow the rules below in full: lead with the next action, number multi-step work, restate state across turns, suppress tangents, give specific time estimates, make wins visible, and cut all preamble and closers.

<!-- Generated from skills/i-have-adhd/SKILL.md by scripts/build_claude_md.sh. Do not edit by hand. -->

HEADER

# Strip the leading YAML frontmatter block (--- ... --- at the very top of the
# file), then drop the body's own `# i-have-adhd` H1 and the blank lines around
# it, since the header above already supplies an H1.
#
# An unterminated fence is not frontmatter, so the whole file is kept unless the
# closing delimiter exists. That two-pass read (hence the file passed twice)
# mirrors hooks/always-on.{sh,mjs,ps1}; keep the three in step, since a single
# pass would treat a leading horizontal rule as an unclosed frontmatter block
# and swallow the entire ruleset.
awk '
  NR == FNR {
    if (NR == 1 && $0 ~ /^---[[:space:]]*$/) { in_fm = 1; next }
    if (in_fm && $0 ~ /^---[[:space:]]*$/)   { in_fm = 0; closed = 1 }
    next
  }

  FNR == 1 { strip = closed }
  strip && FNR == 1 && $0 ~ /^---[[:space:]]*$/ { skipping = 1; next }
  skipping && $0 ~ /^---[[:space:]]*$/          { skipping = 0; next }
  skipping                                      { next }

  !dropped_h1 && $0 ~ /^# /            { dropped_h1 = 1; next }
  !body && $0 ~ /^[[:space:]]*$/       { next }

  { body = 1; print }

  END {
    if (!body) {
      print "build_claude_md.sh: SKILL.md has no body to copy" > "/dev/stderr"
      exit 1
    }
  }
' "$skill_path" "$skill_path"
