#!/usr/bin/env sh
# SessionStart hook: injects the full i-have-adhd ruleset when the user has
# opted in by creating $CLAUDE_CONFIG_DIR/.i-have-adhd-always (default ~/.claude).
# Never blocks session start: any failure exits 0.
#
# POSIX fallback for environments where the default Node hook cannot run. It
# works with sh on macOS/Linux and Git Bash on Windows without a Node install.

# ⚠ Look in every config dir the user could have created it in, not just one.
# Claude Code supports a per-project CLAUDE_CONFIG_DIR, and a common setup
# points it at a directory that symlinks settings.json/hooks/commands back to
# ~/.claude without mirroring everything else. The flag then stays a real file
# in ~/.claude, is never found, and this hook exits 0 — indistinguishable from
# a deliberate opt-out. Measured on one such setup: 2,061 invocations of this
# plugin, every one emitting zero bytes.
flag_path=""
for candidate_dir in "$CLAUDE_CONFIG_DIR" "$HOME/.claude" "$XDG_CONFIG_HOME/claude"; do
  [ -n "$candidate_dir" ] || continue
  if [ -f "$candidate_dir/.i-have-adhd-always" ]; then
    flag_path="$candidate_dir/.i-have-adhd-always"
    break
  fi
done

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
