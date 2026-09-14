// Codex-only SessionStart wrapper. Codex requires SessionStart hooks to emit
// either empty stdout or a single JSON envelope, unlike Claude Code, which
// accepts always-on.mjs's plain-text output directly. This captures that
// plain text and re-emits it wrapped, without changing always-on.mjs itself.
import path from "node:path";
import { pathToFileURL } from "node:url";

const root = process.env.CLAUDE_PLUGIN_ROOT || process.env.PLUGIN_ROOT;
if (!root) process.exit(0);

const chunks = [];
const originalWrite = process.stdout.write.bind(process.stdout);
process.stdout.write = (chunk) => {
  chunks.push(chunk);
  return true;
};

try {
  await import(pathToFileURL(path.join(root, "hooks", "always-on.mjs")).href);
} finally {
  process.stdout.write = originalWrite;
}

const text = chunks.join("");
if (text) {
  process.stdout.write(
    JSON.stringify({
      hookSpecificOutput: { hookEventName: "SessionStart", additionalContext: text },
    }),
  );
}
