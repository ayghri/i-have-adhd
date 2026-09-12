import { existsSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import {
  getAgentDir,
  type ExtensionAPI,
  type ExtensionContext,
} from "@earendil-works/pi-coding-agent";
import {
  contextMessages,
  latestMarkerIsActive,
} from "./context-compat";

const EXTENSION_DIR = dirname(fileURLToPath(import.meta.url));
const SKILL_PATH = join(
  EXTENSION_DIR,
  "..",
  "skills",
  "i-have-adhd",
  "SKILL.md",
);
const STATE_ENTRY_TYPE = "i-have-adhd-state";
const RULES_MESSAGE_TYPE = "i-have-adhd-rules";
const DISABLED_MESSAGE_TYPE = "i-have-adhd-disabled";
const MODE_MESSAGE_TYPE = "i-have-adhd-mode-changed";
const STATUS_KEY = "i-have-adhd";
const DISABLE_CONFIRMATION = "ADHD mode disabled.";
const STOP_PHRASES = new Set(["stop adhd mode", "normal mode"]);
const RULES_HEADER =
  'ADHD MODE ACTIVE. The ruleset below applies to every response until turned off. "stop adhd mode" or "normal mode" turns it off for this session.';
const DISABLED_NOTICE =
  "ADHD MODE OFF. Ignore the i-have-adhd ruleset injected earlier in this conversation and return to your default response style.";

// Matches the four modes named in the skill's "Response Mode" section.
// Keep this list in sync with that section if it ever changes.
const RESPONSE_MODES = ["compact", "normal", "deep", "audit"] as const;
type ResponseMode = (typeof RESPONSE_MODES)[number];

function isResponseMode(value: unknown): value is ResponseMode {
  return (
    typeof value === "string" &&
    (RESPONSE_MODES as readonly string[]).includes(value)
  );
}

function modeDirective(mode: ResponseMode): string {
  return `Response Mode is explicitly set to "${mode}" for the rest of this session (see "Response Mode" in the ruleset). This overrides the automatic classifier until changed with /i-have-adhd <mode> or the session ends.`;
}

type AdhdModeState = {
  enabled: boolean;
  mode?: ResponseMode;
};

type AdhdConfig = {
  alwaysOn?: boolean;
  hideStatus?: boolean;
};

function loadConfig(): AdhdConfig {
  try {
    return JSON.parse(
      readFileSync(join(getAgentDir(), "i-have-adhd.json"), "utf8"),
    );
  } catch {
    return {};
  }
}

function stripFrontmatter(content: string): string {
  return content
    .replace(
      /^---[^\S\r\n]*\r?\n[\s\S]*?\r?\n---[^\S\r\n]*(?:\r?\n|$)/,
      "",
    )
    .trim();
}

function loadRules(): string {
  let content: string;

  try {
    content = readFileSync(SKILL_PATH, "utf8");
  } catch (error) {
    const reason = error instanceof Error ? error.message : String(error);
    throw new Error(
      `Unable to load i-have-adhd rules from ${SKILL_PATH}: ${reason}`,
    );
  }

  const rules = stripFrontmatter(content);
  if (!rules) {
    throw new Error(`The i-have-adhd rules file is empty: ${SKILL_PATH}`);
  }

  return rules;
}

function getSavedState(ctx: ExtensionContext): AdhdModeState | undefined {
  let savedState: AdhdModeState | undefined;

  for (const entry of ctx.sessionManager.getBranch()) {
    if (entry.type !== "custom" || entry.customType !== STATE_ENTRY_TYPE) {
      continue;
    }

    const data = entry.data as Partial<AdhdModeState> | undefined;
    if (typeof data?.enabled === "boolean") {
      // Older entries (written before mode support existed) never set
      // `mode`; carry the previously seen mode forward instead of
      // resetting it, so a mode chosen earlier in the branch survives a
      // later plain on/off toggle that doesn't mention mode at all.
      savedState = {
        enabled: data.enabled,
        mode: isResponseMode(data.mode) ? data.mode : savedState?.mode,
      };
    }
  }

  return savedState;
}

/**
 * Whether the rules are still live in the context the model actually receives.
 *
 * Only the newest marker counts: a later "disabled" notice cancels an earlier
 * ruleset, and compaction drops summarized entries so the ruleset has to be
 * injected again.
 */
function rulesAreInContext(ctx: ExtensionContext): boolean {
  return latestMarkerIsActive(
    contextMessages(ctx.sessionManager),
    RULES_MESSAGE_TYPE,
    DISABLED_MESSAGE_TYPE,
  );
}

export default function iHaveAdhdExtension(pi: ExtensionAPI) {
  const rules = loadRules();
  const alwaysOnFlag = join(getAgentDir(), ".i-have-adhd-always");
  const config = loadConfig();
  let enabled = false;
  let mode: ResponseMode | undefined;

  const updateStatus = (ctx: ExtensionContext): void => {
    if (!enabled || config.hideStatus) {
      ctx.ui.setStatus(STATUS_KEY, undefined);
      return;
    }

    const dot = ctx.ui.theme.fg("success", "●");
    const label = ctx.ui.theme.fg("accent", mode ? `ADHD ON [${mode}]` : "ADHD ON");
    ctx.ui.setStatus(STATUS_KEY, `${dot} ${label}`);
  };

  /**
   * Keep the conversation in sync with the current mode, the way the Claude Code
   * SessionStart hook does: inject the ruleset once, never per request.
   */
  const syncContext = (ctx: ExtensionContext): void => {
    const injected = rulesAreInContext(ctx);

    if (enabled && !injected) {
      // Fold the active response mode into the same injection instead of a
      // separate marker: this is the one point where the ruleset (and so
      // the mode) has to survive compaction, so there is nothing extra to
      // keep synchronized after this.
      const modeNote = mode ? `\n\n${modeDirective(mode)}` : "";
      pi.sendMessage(
        {
          customType: RULES_MESSAGE_TYPE,
          content: `${RULES_HEADER}\n\n${rules}${modeNote}`,
          display: false,
        },
        { triggerTurn: false },
      );
      return;
    }

    if (!enabled && injected) {
      pi.sendMessage(
        {
          customType: DISABLED_MESSAGE_TYPE,
          content: DISABLED_NOTICE,
          display: false,
        },
        { triggerTurn: false },
      );
    }
  };

  const restoreState = (ctx: ExtensionContext): void => {
    const savedState = getSavedState(ctx);
    const enabledByDefault =
      pi.getFlag("adhd") === true ||
      config.alwaysOn === true ||
      existsSync(alwaysOnFlag);

    enabled = savedState?.enabled ?? enabledByDefault;
    mode = savedState?.mode;
    updateStatus(ctx);
    syncContext(ctx);
  };

  const setEnabled = (nextEnabled: boolean, ctx: ExtensionContext): void => {
    enabled = nextEnabled;
    pi.appendEntry(STATE_ENTRY_TYPE, { enabled, mode } satisfies AdhdModeState);
    updateStatus(ctx);
    syncContext(ctx);
    ctx.ui.notify(`ADHD mode ${enabled ? "enabled" : "disabled"}`, "info");
  };

  const setMode = (nextMode: ResponseMode, ctx: ExtensionContext): void => {
    mode = nextMode;
    // Setting a mode implies wanting the ruleset active; a mode with the
    // ruleset off would have nothing to modify.
    enabled = true;
    pi.appendEntry(STATE_ENTRY_TYPE, { enabled, mode } satisfies AdhdModeState);
    updateStatus(ctx);
    syncContext(ctx);

    // If the ruleset was already injected this session, syncContext above
    // does nothing (it only (re-)injects when missing) -- send the mode
    // change on its own so the model sees it without waiting for the next
    // compaction-triggered re-injection.
    if (rulesAreInContext(ctx)) {
      pi.sendMessage(
        {
          customType: MODE_MESSAGE_TYPE,
          content: modeDirective(nextMode),
          display: false,
        },
        { triggerTurn: false },
      );
    }

    ctx.ui.notify(`ADHD response mode: ${nextMode}`, "info");
  };

  pi.registerFlag("adhd", {
    description: "Start with ADHD-friendly output enabled",
    type: "boolean",
    default: false,
  });

  pi.registerCommand("i-have-adhd", {
    description:
      "Toggle ADHD-friendly output, or set a response mode (compact/normal/deep/audit)",
    handler: async (args, ctx) => {
      const argument = args.trim().toLowerCase();

      if (argument === "") {
        setEnabled(!enabled, ctx);
        return;
      }

      if (argument === "on") {
        setEnabled(true, ctx);
        return;
      }

      if (argument === "off" || argument === "stop") {
        setEnabled(false, ctx);
        return;
      }

      if (isResponseMode(argument)) {
        setMode(argument, ctx);
        return;
      }

      ctx.ui.notify(
        "Usage: /i-have-adhd [on|off|compact|normal|deep|audit]",
        "warning",
      );
    },
  });

  pi.on("input", async (event, ctx) => {
    const input = event.text.trim().toLowerCase();

    // Keep the built-in skill command working as an alias without letting Pi
    // expand a second copy of the same rules into the conversation.
    if (input === "/skill:i-have-adhd") {
      setEnabled(true, ctx);
      return { action: "handled" };
    }

    if (enabled && STOP_PHRASES.has(input)) {
      setEnabled(false, ctx);

      if (ctx.hasUI) {
        return { action: "handled" };
      }

      return {
        action: "transform",
        text: `Reply with exactly: ${DISABLE_CONFIRMATION}`,
      };
    }

    return { action: "continue" };
  });

  pi.on("session_start", async (_event, ctx) => restoreState(ctx));
  pi.on("session_tree", async (_event, ctx) => restoreState(ctx));
  pi.on("session_compact", async (_event, ctx) => syncContext(ctx));
}
