#!/usr/bin/env node
// Regenerates skills/i-have-adhd/rules.md from skills/i-have-adhd/SKILL.md.
//
// This is the one place that parses the SKILL.md frontmatter. The five
// entry points (hooks/always-on.mjs, hooks/always-on.sh,
// hooks/always-on.ps1, extensions/i-have-adhd.ts,
// scripts/render_gemini_command.py) just read the generated rules.md
// verbatim, so a frontmatter-parsing bug only needs fixing here.
//
// Run after editing SKILL.md. Pass --check to verify the checked-in
// rules.md matches without writing it, the same --check convention
// scripts/render_gemini_command.py and scripts/render_manifests.py use.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const skillPath = path.join(scriptDir, "..", "skills", "i-have-adhd", "SKILL.md");
const rulesPath = path.join(scriptDir, "..", "skills", "i-have-adhd", "rules.md");

// Strip a leading YAML frontmatter block (--- ... --- at the very top of
// file). An unterminated fence is not frontmatter, so the whole file is
// kept unless the closing delimiter exists.
function stripFrontmatter(content) {
  return content
    .replace(/^---[^\S\r\n]*\r?\n[\s\S]*?\r?\n---[^\S\r\n]*(?:\r?\n|$)/, "")
    .replace(/(?:\r?\n)+$/, "");
}

const source = fs.readFileSync(skillPath, "utf8");
const rules = stripFrontmatter(source);

if (!rules) {
  throw new Error(`Stripping frontmatter left no content: ${skillPath}`);
}

const rendered = `${rules}\n`;

if (process.argv.slice(2).includes("--check")) {
  const current = fs.existsSync(rulesPath)
    ? fs.readFileSync(rulesPath, "utf8")
    : null;
  if (current !== rendered) {
    console.error(
      `${rulesPath} is out of sync with ${skillPath}.\n` +
        "Run: node scripts/generate_rules.mjs",
    );
    process.exit(1);
  }
  console.log("rules.md matches SKILL.md");
} else {
  fs.writeFileSync(rulesPath, rendered);
}
