// SessionStart hook: injects the full i-have-adhd ruleset when the user has
// opted in by creating the flag file (default ~/.claude/.i-have-adhd-always)
// and the session is human. Unclear sessions get a one-line notice instead.
// Never blocks session start: any failure exits 0.
//
// Runs under Node so it works on macOS, Linux, and Windows. The shared Claude
// Code/Codex hook launches this module from the plugin-root environment rather
// than relying on platform-specific shell expansion for the script path.
// Native sh and PowerShell implementations remain available as fallbacks.
//
// Launchers pass `--agent claude|codex`; `--json` renders the structured Codex
// SessionStart envelope (or the plain systemMessage notice).

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  NOTICE,
  classifySession,
  flagPathFor,
  logDecision,
  parentArgv,
} from "./session-kind.mjs";

function argument(name, fallback = null) {
  const index = process.argv.indexOf(name);
  return index >= 0 && process.argv[index + 1] ? process.argv[index + 1] : fallback;
}

try {
  const agent = argument("--agent", "claude");
  const json = process.argv.includes("--json");
  const flagPath = flagPathFor(agent);

  // Only fire when the user has opted in.
  if (!flagPath || !fs.existsSync(flagPath)) process.exit(0);

  const decision = classifySession({
    agent,
    env: process.env,
    parent: agent === "codex" ? parentArgv() : null,
  });
  logDecision({ agent, ...decision, flagPath });

  if (decision.decision === "opt-out" || decision.decision === "non-human") {
    process.exit(0);
  }

  if (decision.decision === "unclear") {
    process.stdout.write(JSON.stringify({ systemMessage: NOTICE }));
    process.exit(0);
  }

  // Resolve SKILL.md relative to this script's own location, not a trusted env var.
  const scriptDir = path.dirname(fileURLToPath(import.meta.url));
  const skillPath = path.join(scriptDir, "..", "skills", "i-have-adhd", "SKILL.md");
  if (!fs.existsSync(skillPath)) process.exit(0);

  // Strip a leading YAML frontmatter block (--- ... --- at the very top of file).
  // Read as raw UTF-8: Codex compares the context bytes and CRLF must survive.
  const body = fs
    .readFileSync(skillPath, "utf8")
    .replace(
      /^---[^\S\r\n]*\r?\n[\s\S]*?\r?\n---[^\S\r\n]*(?:\r?\n|$)/,
      "",
    )
    .replace(/(?:\r?\n)+$/, "");

  const header =
    'ADHD MODE ACTIVE (always-on). The ruleset below applies to every response. ' +
    '"stop adhd mode" turns it off for this session; ' +
    `delete ${flagPath} to turn always-on off for good.`;

  if (json) {
    process.stdout.write(
      JSON.stringify({
        hookSpecificOutput: {
          hookEventName: "SessionStart",
          additionalContext: `${header}\n\n${body}`,
        },
      }),
    );
  } else {
    process.stdout.write(`${header}\n\n${body}\n`);
  }
} catch {
  // Never block session start.
  process.exit(0);
}
