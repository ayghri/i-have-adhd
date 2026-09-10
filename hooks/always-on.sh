#!/usr/bin/env sh
# SessionStart hook: injects the full i-have-adhd ruleset at the start of every
# session once always-on is turned on. Off by default. Any one of these turns
# it on: the flag file $CLAUDE_CONFIG_DIR/.i-have-adhd-always (default
# ~/.claude), the plugin option "always_on" (exported to hooks as
# CLAUDE_PLUGIN_OPTION_ALWAYS_ON), or the environment variable
# I_HAVE_ADHD_ALWAYS_ON. $CLAUDE_CONFIG_DIR/.i-have-adhd-off wins over all.
# Never blocks session start: any failure exits 0.
#
# POSIX fallback for environments where the default Node hook cannot run. It
# works with sh on macOS/Linux and Git Bash on Windows without a Node install.

claude_dir="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
off_path="$claude_dir/.i-have-adhd-off"
always_path="$claude_dir/.i-have-adhd-always"

# Explicit opt-out wins over every way of opting in.
[ -f "$off_path" ] && exit 0

truthy() {
  case "$(printf '%s' "${1:-}" | tr '[:upper:]' '[:lower:]' | tr -d '[:space:]')" in
    1|true|yes|on) return 0 ;;
    *) return 1 ;;
  esac
}
if [ ! -f "$always_path" ] && ! truthy "${CLAUDE_PLUGIN_OPTION_ALWAYS_ON:-}" && ! truthy "${I_HAVE_ADHD_ALWAYS_ON:-}"; then
  exit 0
fi

# Also silent when settings.json selects the plugin's output style: the rules
# are already in the system prompt (with or without a plugin prefix).
settings_path="$claude_dir/settings.json"
if [ -f "$settings_path" ] && grep -Eq '"outputStyle"[[:space:]]*:[[:space:]]*"([^"]*:)?i-have-adhd"' "$settings_path"; then
  exit 0
fi

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

printf 'ADHD MODE ACTIVE (always-on). The ruleset below applies to every response. "stop adhd mode" turns it off for this session; create %s to turn always-on off for good.\n\n%s\n' \
  "$off_path" "$body"
