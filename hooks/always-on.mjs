// SessionStart hook: injects the full i-have-adhd ruleset when the user has
// opted in by creating a .i-have-adhd-always flag. Claude Code and Codex
// look in $CLAUDE_CONFIG_DIR (default ~/.claude); Copilot sessions (VS Code,
// Copilot CLI) pass I_HAVE_ADHD_CLIENT=copilot and look in $COPILOT_HOME
// (default ~/.copilot). Never blocks session start: any failure exits 0.
//
// Runs under Node so it works on macOS, Linux, and Windows. The shared
// launcher of each harness starts this module from the plugin-root
// environment rather than relying on platform-specific shell expansion for
// the script path. Native sh and PowerShell implementations remain available
// as fallbacks.

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

try {
  const isCopilot = process.env.I_HAVE_ADHD_CLIENT === "copilot";
  const configDir = isCopilot
    ? process.env.COPILOT_HOME || path.join(os.homedir(), ".copilot")
    : process.env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), ".claude");
  const flagPath = path.join(configDir, ".i-have-adhd-always");

  // Only fire when the user has opted in.
  if (!fs.existsSync(flagPath)) process.exit(0);

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

  process.stdout.write(
    "ADHD MODE ACTIVE (always-on). The ruleset below applies to every response. " +
      '"stop adhd mode" turns it off for this session; ' +
      `delete ${flagPath} to turn always-on off for good.\n\n${body}\n`,
  );
} catch {
  // Never block session start.
  process.exit(0);
}
