// SessionStart hook: injects the full i-have-adhd ruleset when the user has
// opted in by creating a .i-have-adhd-always flag in the active host's config
// directory (Claude: CLAUDE_CONFIG_DIR or ~/.claude; Codex: CODEX_HOME or
// ~/.codex).
// Never blocks session start: any failure exits 0.
//
// Runs under Node so it works on macOS, Linux, and Windows. The shared Claude
// Code/Codex hook launches this module from the plugin-root environment rather
// than relying on platform-specific shell expansion for the script path.
// Native sh and PowerShell implementations remain available as fallbacks.

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

try {
  const configuredDir = process.env.CLAUDE_CONFIG_DIR || process.env.CODEX_HOME;
  const configDirs = configuredDir
    ? [configuredDir]
    : [path.join(os.homedir(), ".claude"), path.join(os.homedir(), ".codex")];
  const flagPath = configDirs
    .map((configDir) => path.join(configDir, ".i-have-adhd-always"))
    .find((candidate) => fs.existsSync(candidate));

  // Only fire when the user has opted in.
  if (!flagPath) process.exit(0);

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
