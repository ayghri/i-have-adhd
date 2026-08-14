import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

try {
  const claudeDir = process.env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), ".claude");
  const flagPath = path.join(claudeDir, ".i-have-adhd-always");
  if (!fs.existsSync(flagPath)) process.exit(0);

  const skillPath = path.join(
    path.dirname(fileURLToPath(import.meta.url)),
    "..",
    "skills",
    "i-have-adhd",
    "SKILL.md",
  );
  if (!fs.existsSync(skillPath)) process.exit(0);

  const body = fs
    .readFileSync(skillPath, "utf8")
    .replace(/^---[^\S\r\n]*\r?\n[\s\S]*?\r?\n---[^\S\r\n]*(?:\r?\n|$)/, "")
    .replace(/(?:\r?\n)+$/, "");
  process.stdout.write(
    "ADHD MODE ACTIVE (always-on). The ruleset below applies to every response. " +
      '"stop adhd mode" turns it off for this session; ' +
      `delete ${flagPath} to turn always-on off for good.\n\n${body}\n`,
  );
} catch {
  process.exit(0);
}
