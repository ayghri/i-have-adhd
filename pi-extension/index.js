// i-have-adhd — Pi agent extension
//
// Registers /i-have-adhd as a native slash command, injects the full ruleset
// into the system prompt when active, shows a status-bar indicator, and
// supports always-on via a flag file (~/.pi/.i-have-adhd-always).
//
// "stop adhd mode" or "normal mode" turns it off for the session.

import { readFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { homedir } from "node:os";

const __dirname = dirname(fileURLToPath(import.meta.url));
const SKILL_PATH = join(__dirname, "..", "skills", "i-have-adhd", "SKILL.md");

// -- Helpers --

/**
 * Strip YAML frontmatter (--- ... ---) from the top of a Markdown file.
 * Returns the body as-is if no frontmatter is present.
 */
function stripFrontmatter(text) {
  return String(text || "").replace(/^---[\s\S]*?---\s*/, "");
}

/**
 * Read the SKILL.md body (without frontmatter).
 * Falls back to a compact ruleset if the file is unreadable.
 */
function getInstructions() {
  try {
    return stripFrontmatter(readFileSync(SKILL_PATH, "utf8"));
  } catch {
    return getFallbackInstructions();
  }
}

function getFallbackInstructions() {
  return [
    "ADHD MODE ACTIVE.",
    "",
    "The reader has ADHD. Output is not just brief; it is shaped so an ADHD brain can act on it.",
    "",
    "## Rules",
    "",
    "1. Lead with the next action. The first line is something the reader can do.",
    "2. Number multi-step tasks. One bounded action per step.",
    "3. End with one concrete next action doable in under two minutes.",
    "4. Suppress tangents. Finish the first issue before raising a second.",
    '5. Restate state every turn ("Step 3 of 5 done: ... Next: ...").',
    "6. Give specific time estimates (minutes, not \"a bit\").",
    "7. Make completed work visible in concrete terms.",
    '8. Matter-of-fact tone for errors: cause, then fix. No "uh oh".',
    "9. Cap lists at 5 items.",
    "10. No preamble, no recap, no closing pleasantries.",
    "",
    'Turn off: "stop adhd mode" or "normal mode".',
  ].join("\n");
}

/**
 * "stop adhd mode" / "normal mode" turn the rules off, but only as a standalone
 * command. Matching the phrase anywhere in the message turned it off mid-task
 * for ordinary requests — so require the whole message to be the command,
 * ignoring case and trailing punctuation.
 */
function isDeactivationCommand(text) {
  const t = String(text || "").trim().toLowerCase().replace(/[.!?\s]+$/, "");
  return t === "stop adhd mode" || t === "normal mode";
}

/**
 * Check for the always-on flag file.
 * Resolution order:
 *   1. I_HAVE_ADHD_ALWAYS env var (truthy = always on)
 *   2. ~/.pi/.i-have-adhd-always flag file
 */
function isAlwaysOn() {
  const env = process.env.I_HAVE_ADHD_ALWAYS;
  if (env !== undefined) {
    const v = env.trim().toLowerCase();
    return v !== "" && v !== "0" && v !== "false" && v !== "no";
  }
  try {
    readFileSync(join(homedir(), ".pi", ".i-have-adhd-always"));
    return true;
  } catch {
    return false;
  }
}

/**
 * Resolve the session's active state from persisted entries.
 */
function resolveSessionActive(entries) {
  if (!Array.isArray(entries)) return null;
  for (let i = entries.length - 1; i >= 0; i -= 1) {
    const entry = entries[i];
    if (entry?.type !== "custom" || entry?.customType !== "adhd-mode") continue;
    return entry?.data?.active === true;
  }
  return null;
}

export { isDeactivationCommand, isAlwaysOn, getInstructions, stripFrontmatter };

export default function adhdExtension(pi) {
  let isActive = false;
  let lastCtx = null;

  // -- Status bar --
  function syncStatus(ctx) {
    if (ctx) lastCtx = ctx;
    const c = ctx || lastCtx;
    if (!c?.ui?.setStatus) return;
    let theme;
    try {
      theme = c.ui.theme;
      if (!theme?.fg) return;
    } catch {
      return;
    }
    if (!isActive) {
      c.ui.setStatus("i-have-adhd", "");
      return;
    }
    const indicator = theme.fg("accent", "●");
    c.ui.setStatus(
      "i-have-adhd",
      indicator + " " + theme.fg("muted", "adhd: ") + theme.fg("text", "ON"),
    );
  }

  const setActive = (active, ctx) => {
    isActive = active;
    pi.appendEntry("adhd-mode", { active });
    syncStatus(ctx);
  };

  // -- /i-have-adhd command --
  pi.registerCommand("i-have-adhd", {
    description:
      "Toggle ADHD-friendly output. Commands: on, off, status. No args = on.",
    handler: async (args, ctx) => {
      const normalized = String(args || "").trim().toLowerCase();

      if (normalized === "status") {
        ctx?.ui?.notify?.(
          `i-have-adhd: ${isActive ? "ON" : "OFF"} • always-on: ${isAlwaysOn() ? "yes" : "no"}`,
          "info",
        );
        return;
      }

      if (normalized === "off" || normalized === "stop") {
        setActive(false, ctx);
        ctx?.ui?.notify?.("ADHD mode OFF. Back to default style.", "info");
        return;
      }

      // No args or "on" → activate
      if (normalized === "" || normalized === "on") {
        setActive(true, ctx);
        ctx?.ui?.notify?.(
          "ADHD mode ON. Rules apply to every response. Say \"stop adhd mode\" to turn off.",
          "info",
        );
        return;
      }

      ctx?.ui?.notify?.(
        "Unknown command. Use: /i-have-adhd on | off | status",
        "warning",
      );
    },
  });

  // -- Deactivation via natural language --
  pi.on("input", async (event) => {
    if (event?.source === "extension") return;
    const text = String(event?.text || "");
    if (isActive && isDeactivationCommand(text)) {
      setActive(false);
    }
  });

  // -- Session start: check always-on --
  pi.on("session_start", async (_event, ctx) => {
    const entries =
      ctx?.sessionManager?.getBranch?.() || ctx?.sessionManager?.getEntries?.() || [];
    const persisted = resolveSessionActive(entries);

    // Persisted explicit choice wins; otherwise check always-on flag
    isActive = persisted !== null ? persisted : isAlwaysOn();
    syncStatus(ctx);

    if (isActive) {
      ctx?.ui?.notify?.(
        `i-have-adhd: ${persisted !== null ? "resumed" : "always-on"}. Say "stop adhd mode" to turn off.`,
        "info",
      );
    }
  });

  pi.on("agent_start", async (_event, ctx) => {
    syncStatus(ctx);
  });

  pi.on("agent_end", async (_event, ctx) => {
    syncStatus(ctx);
  });

  // -- Inject rules into system prompt --
  pi.on("before_agent_start", async (event) => {
    if (!isActive) return;
    const base = event?.systemPrompt ? `${event.systemPrompt}\n\n` : "";
    return {
      systemPrompt: `${base}ADHD MODE ACTIVE — i-have-adhd\n\n${getInstructions()}`,
    };
  });
}
