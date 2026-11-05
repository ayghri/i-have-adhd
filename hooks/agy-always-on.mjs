// Antigravity's SessionStart expects JSON rather than Claude's plain text.
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

let result = {};
try {
  const flag = path.join(os.homedir(), ".gemini", "antigravity-cli", ".i-have-adhd-always");
  if (fs.existsSync(flag)) {
    const skill = path.join(path.dirname(fileURLToPath(import.meta.url)), "..", "skills", "i-have-adhd", "SKILL.md");
    const body = fs.readFileSync(skill, "utf8")
      .replace(/^---[^\S\r\n]*\r?\n[\s\S]*?\r?\n---[^\S\r\n]*(?:\r?\n|$)/, "")
      .replace(/(?:\r?\n)+$/, "");
    result = { injectSteps: [{ userMessage: `ADHD MODE ACTIVE (always-on). Delete the Antigravity always-on flag to turn this off for future sessions.\n\n${body}\n` }] };
  }
} catch {
  // A missing flag, skill, or inaccessible file must not block the session.
}
process.stdout.write(JSON.stringify(result));
