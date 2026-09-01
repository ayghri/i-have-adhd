// SessionStart hook: injects the full i-have-adhd ruleset when the user has
// opted in by creating $CLAUDE_CONFIG_DIR/.i-have-adhd-always (default ~/.claude).
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
  // Look in every config dir the user could have created it in, not just one.
  // Claude Code supports a per-project CLAUDE_CONFIG_DIR, and a common setup
  // points it at a directory that symlinks settings.json/hooks/commands back to
  // ~/.claude without mirroring everything else. The flag then stays a real file
  // in ~/.claude, is never found, and this hook exits 0 — indistinguishable from
  // a deliberate opt-out. Measured on one such setup: 2,061 invocations of this
  // plugin, every one emitting zero bytes.
  const candidateDirs = [
    process.env.CLAUDE_CONFIG_DIR,
    path.join(os.homedir(), ".claude"),
    process.env.XDG_CONFIG_HOME && path.join(process.env.XDG_CONFIG_HOME, "claude"),
  ].filter(Boolean);

  const flagPath = candidateDirs
    .map((dir) => path.join(dir, ".i-have-adhd-always"))
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
