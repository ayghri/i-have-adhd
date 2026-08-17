// SessionStart hook: injects the full i-have-adhd ruleset when the user has
// opted in by creating $CLAUDE_CONFIG_DIR/.i-have-adhd-always (default ~/.claude).
// Never blocks session start: any failure exits 0.
//
// Runs under Node so it works on macOS, Linux, and Windows. The shared Claude
// Code/Codex hook launches this module from the plugin-root environment rather
// than relying on platform-specific shell expansion for the script path.
// Native sh and PowerShell implementations remain available as fallbacks.
//
// Reads skills/i-have-adhd/rules.md verbatim: frontmatter parsing happens
// once, at build time, in scripts/generate_rules.mjs.
//
// The banner text is shared with the other two runtimes via banner.txt
// (line 1 = prefix, line 2 = suffix) instead of being hand-authored three
// times, once per runtime's string-escaping dialect.

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

try {
  const claudeDir = process.env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), ".claude");
  const flagPath = path.join(claudeDir, ".i-have-adhd-always");

  // Only fire when the user has opted in.
  if (!fs.existsSync(flagPath)) process.exit(0);

  // Resolve rules.md and banner.txt relative to this script's own location,
  // not a trusted env var.
  const scriptDir = path.dirname(fileURLToPath(import.meta.url));
  const rulesPath = path.join(scriptDir, "..", "skills", "i-have-adhd", "rules.md");
  if (!fs.existsSync(rulesPath)) process.exit(0);

  const body = fs.readFileSync(rulesPath, "utf8").replace(/(?:\r?\n)+$/, "");
  const bannerTemplate = fs
    .readFileSync(path.join(scriptDir, "banner.txt"), "utf8")
    .replace(/(?:\r?\n)+$/, "");
  const token = "{{FLAG_PATH}}";
  const tokenIndex = bannerTemplate.indexOf(token);
  const banner =
    bannerTemplate.slice(0, tokenIndex) + flagPath + bannerTemplate.slice(tokenIndex + token.length);

  process.stdout.write(`${banner}\n\n${body}\n`);
} catch {
  // Never block session start.
  process.exit(0);
}
