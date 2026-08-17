#!/usr/bin/env sh
# SessionStart hook: injects the full i-have-adhd ruleset when the user has
# opted in by creating $CLAUDE_CONFIG_DIR/.i-have-adhd-always (default ~/.claude).
# Never blocks session start: any failure exits 0.
#
# POSIX fallback for environments where the default Node hook cannot run. It
# works with sh on macOS/Linux and Git Bash on Windows without a Node install.
#
# Reads skills/i-have-adhd/rules.md verbatim: frontmatter parsing happens
# once, at build time, in scripts/generate_rules.mjs.
#
# The banner text is shared with the other two runtimes via banner.txt,
# which carries a {{FLAG_PATH}} placeholder that each runtime splices its
# own flag path into, instead of being hand-authored three times, once per
# runtime's string-escaping dialect.

claude_dir="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
flag_path="$claude_dir/.i-have-adhd-always"

# Only fire when the user has opted in.
[ -f "$flag_path" ] || exit 0

# $0 is the absolute script path substituted into hooks.json by Claude Code,
# so resolve rules.md and banner.txt relative to it instead of trusting an
# exported env var.
script_dir=$(dirname -- "$0")
rules_path="$script_dir/../skills/i-have-adhd/rules.md"
banner_path="$script_dir/banner.txt"
[ -f "$rules_path" ] || exit 0

body=$(cat "$rules_path") || exit 0
# Splice the flag path into the shared template at the literal
# {{FLAG_PATH}} token. Quoted parts of a pattern match literally in POSIX
# sh, so a flag path full of special characters cannot break the split.
banner_template=$(cat "$banner_path") || exit 0
token='{{FLAG_PATH}}'
banner_prefix=${banner_template%%"$token"*}
banner_suffix=${banner_template#*"$token"}

printf '%s%s%s\n\n%s\n' "$banner_prefix" "$flag_path" "$banner_suffix" "$body"
