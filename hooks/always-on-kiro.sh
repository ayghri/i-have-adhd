#!/usr/bin/env sh
# agentSpawn hook: injects the full i-have-adhd ruleset when the user has
# opted in by creating $KIRO_CONFIG_DIR/.i-have-adhd-always (default ~/.kiro).
# Never blocks agent spawn: any failure exits 0.
#
# Install — add to your Kiro agent config (e.g. ~/.kiro/agents/default.json):
#
#   {
#     "hooks": {
#       "agentSpawn": [
#         { "command": "/path/to/i-have-adhd/hooks/always-on-kiro.sh" }
#       ]
#     }
#   }
#
# Opt in:   touch ~/.kiro/.i-have-adhd-always
# Opt out:  rm ~/.kiro/.i-have-adhd-always

kiro_dir="${KIRO_CONFIG_DIR:-$HOME/.kiro}"
flag_path="$kiro_dir/.i-have-adhd-always"

# Only fire when the user has opted in.
[ -f "$flag_path" ] || exit 0

# $0 is the absolute script path passed by Kiro, so resolve SKILL.md relative
# to it rather than trusting an exported env var.
script_dir=$(dirname -- "$0")
skill_path="$script_dir/../skills/i-have-adhd/SKILL.md"
[ -f "$skill_path" ] || exit 0

# Strip a leading YAML frontmatter block (--- ... --- at the very top of file).
# An unterminated fence is not frontmatter, so the whole file is kept unless the
# closing delimiter exists (two passes; matches the Node and PowerShell hooks).
# Matches the logic in always-on.sh and always-on.mjs.
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
