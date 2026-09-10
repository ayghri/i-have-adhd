#!/usr/bin/env sh
# SessionStart hook: injects the full i-have-adhd ruleset when the user has
# opted in by creating a .i-have-adhd-always flag in the active host's config
# directory (Claude: CLAUDE_CONFIG_DIR or ~/.claude; Codex: CODEX_HOME or
# ~/.codex).
# Never blocks session start: any failure exits 0.
#
# POSIX fallback for environments where the default Node hook cannot run. It
# works with sh on macOS/Linux and Git Bash on Windows without a Node install.

flag_path=""
if [ -n "${CLAUDE_CONFIG_DIR:-}" ]; then
  candidate_flag_path="$CLAUDE_CONFIG_DIR/.i-have-adhd-always"
  [ -f "$candidate_flag_path" ] && flag_path="$candidate_flag_path"
elif [ -n "${CODEX_HOME:-}" ]; then
  candidate_flag_path="$CODEX_HOME/.i-have-adhd-always"
  [ -f "$candidate_flag_path" ] && flag_path="$candidate_flag_path"
else
  for config_dir in "$HOME/.claude" "$HOME/.codex"; do
    candidate_flag_path="$config_dir/.i-have-adhd-always"
    if [ -f "$candidate_flag_path" ]; then
      flag_path="$candidate_flag_path"
      break
    fi
  done
fi

# Only fire when the user has opted in.
[ -n "$flag_path" ] || exit 0

# $0 is the absolute script path substituted into hooks.json by Claude Code,
# so resolve SKILL.md relative to it instead of trusting an exported env var.
script_dir=$(dirname -- "$0")
skill_path="$script_dir/../skills/i-have-adhd/SKILL.md"
[ -f "$skill_path" ] || exit 0

# Strip a leading YAML frontmatter block (--- ... --- at the very top of file).
# An unterminated fence is not frontmatter, so the whole file is kept unless the
# closing delimiter exists (two passes; matches the Node and PowerShell hooks).
body=$(awk '
  NR == FNR {
    if (NR == 1 && $0 ~ /^---[[:space:]]*$/) { in_fm = 1; next }
    if (in_fm && $0 ~ /^---[[:space:]]*$/)   { in_fm = 0; closed = 1 }
    next
  }
  FNR == 1 { strip = closed }
  strip && FNR == 1 && $0 ~ /^---[[:space:]]*$/ { skipping = 1; next }
  skipping && $0 ~ /^---[[:space:]]*$/          { skipping = 0; next }
  !skipping { print }
' "$skill_path" "$skill_path") || exit 0

printf 'ADHD MODE ACTIVE (always-on). The ruleset below applies to every response. "stop adhd mode" turns it off for this session; delete %s to turn always-on off for good.\n\n%s\n' \
  "$flag_path" "$body"
