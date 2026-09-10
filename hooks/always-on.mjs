// SessionStart / SubagentStart hook: injects the full i-have-adhd ruleset at
// the start of every session once the user has turned always-on on. Off by
// default. Any one of these turns it on:
//   - the flag file $CLAUDE_CONFIG_DIR/.i-have-adhd-always (default ~/.claude)
//   - the plugin option "always_on" (plugin.json userConfig), which Claude Code
//     exports to hooks as CLAUDE_PLUGIN_OPTION_ALWAYS_ON
//   - the environment variable I_HAVE_ADHD_ALWAYS_ON (for harnesses without
//     plugin options, e.g. Codex)
// The file $CLAUDE_CONFIG_DIR/.i-have-adhd-off wins over all of them.
// Never blocks session start: any failure exits 0.
//
// The plugin also ships the same rules as an output style
// (output-styles/i-have-adhd.md). When the user's settings.json selects it,
// the rules already sit in the system prompt, so the SessionStart branch
// stays silent instead of injecting them a second time. Subagents still get
// the ruleset through SubagentStart because they run under their own system
// prompt; the exception is a "fork" subagent, which inherits the parent
// conversation and needs nothing extra.
//
// Runs under Node so it works on macOS, Linux, and Windows. The shared Claude
// Code/Codex hook launches this module from the plugin-root environment rather
// than relying on platform-specific shell expansion for the script path.
// Native sh and PowerShell implementations remain available as fallbacks for
// SessionStart only.
//
// Output shape depends on the event, read from the hook's stdin JSON:
//   SessionStart  -> plain text banner + ruleset (added to context as-is).
//   SubagentStart -> {"hookSpecificOutput":{"hookEventName":"SubagentStart",
//                    "additionalContext": ...}} so the ruleset reaches the
//                    subagent's context, which a SessionStart injection never
//                    does. No stdin, or stdin that is not JSON, is treated as
//                    SessionStart, so direct invocation keeps working.

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

function readEvent() {
  try {
    if (process.stdin.isTTY) return {};
    const raw = fs.readFileSync(0, "utf8");
    if (!raw.trim()) return {};
    const parsed = JSON.parse(raw);
    return parsed && typeof parsed === "object" ? parsed : {};
  } catch {
    return {};
  }
}

// True when settings.json selects this plugin's output style, with or without
// the plugin prefix Claude Code may add ("i-have-adhd:i-have-adhd").
function outputStyleActive(claudeDir) {
  try {
    const raw = fs.readFileSync(path.join(claudeDir, "settings.json"), "utf8");
    let style;
    try {
      style = JSON.parse(raw).outputStyle;
    } catch {
      const m = raw.match(/"outputStyle"\s*:\s*"([^"]*)"/);
      style = m ? m[1] : undefined;
    }
    return typeof style === "string" && /(^|:)i-have-adhd$/.test(style);
  } catch {
    return false;
  }
}

function truthy(value) {
  return typeof value === "string" && ["1", "true", "yes", "on"].includes(value.trim().toLowerCase());
}

try {
  const claudeDir = process.env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), ".claude");
  const offPath = path.join(claudeDir, ".i-have-adhd-off");
  const alwaysPath = path.join(claudeDir, ".i-have-adhd-always");

  // Explicit opt-out wins over every way of opting in.
  if (fs.existsSync(offPath)) process.exit(0);

  const enabled =
    fs.existsSync(alwaysPath) ||
    truthy(process.env.CLAUDE_PLUGIN_OPTION_ALWAYS_ON) ||
    truthy(process.env.I_HAVE_ADHD_ALWAYS_ON);
  if (!enabled) process.exit(0);

  const event = readEvent();
  const eventName =
    typeof event.hook_event_name === "string" ? event.hook_event_name : "SessionStart";

  // Resolve SKILL.md relative to this script's own location, not a trusted env var.
  const scriptDir = path.dirname(fileURLToPath(import.meta.url));
  const skillPath = path.join(scriptDir, "..", "skills", "i-have-adhd", "SKILL.md");
  if (!fs.existsSync(skillPath)) process.exit(0);

  // Strip a leading YAML frontmatter block (--- ... --- at the very top of file).
  const body = fs
    .readFileSync(skillPath, "utf8")
    .replace(
      /^---[^\S\r\n]*\r?\n[\s\S]*?\r?\n---[^\S\r\n]*(?:\r?\n|$)/,
      "",
    )
    .replace(/(?:\r?\n)+$/, "");

  if (eventName === "SubagentStart") {
    // A fork inherits the whole parent conversation, ruleset included.
    if (event.agent_type === "fork") process.exit(0);
    process.stdout.write(
      JSON.stringify({
        hookSpecificOutput: {
          hookEventName: "SubagentStart",
          additionalContext:
            "ADHD MODE ACTIVE (always-on, inherited from the parent session). " +
            `The ruleset below applies to every response.\n\n${body}\n`,
        },
      }) + "\n",
    );
    process.exit(0);
  }

  // The output style already carries the rules in the system prompt.
  if (outputStyleActive(claudeDir)) process.exit(0);

  process.stdout.write(
    "ADHD MODE ACTIVE (always-on). The ruleset below applies to every response. " +
      '"stop adhd mode" turns it off for this session; ' +
      `create ${offPath} to turn always-on off for good.\n\n${body}\n`,
  );
} catch {
  // Never block session start.
  process.exit(0);
}
