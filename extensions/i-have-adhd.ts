import { existsSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import {
  getAgentDir,
  type ExtensionAPI,
  type ExtensionContext,
} from "@earendil-works/pi-coding-agent";
import {
  AdhdMode,
  DISABLED_MESSAGE_TYPE,
  RULES_MESSAGE_TYPE,
  STATE_ENTRY_TYPE,
  isStopPhrase,
  latestEnabledState,
  rulesActiveInContext,
  type Effect,
} from "./state-machine.ts";

const EXTENSION_DIR = dirname(fileURLToPath(import.meta.url));
const RULES_PATH = join(
  EXTENSION_DIR,
  "..",
  "skills",
  "i-have-adhd",
  "rules.md",
);
const STATUS_KEY = "i-have-adhd";
const DISABLE_CONFIRMATION = "ADHD mode disabled.";
const RULES_HEADER =
  'ADHD MODE ACTIVE. The ruleset below applies to every response until turned off. "stop adhd mode" or "normal mode" turns it off for this session.';
const DISABLED_NOTICE =
  "ADHD MODE OFF. Ignore the i-have-adhd ruleset injected earlier in this conversation and return to your default response style.";

// rules.md is generated from SKILL.md by scripts/generate_rules.mjs, which
// is the single place frontmatter parsing happens. Read it verbatim here.
function loadRules(): string {
  let content: string;

  try {
    content = readFileSync(RULES_PATH, "utf8");
  } catch (error) {
    const reason = error instanceof Error ? error.message : String(error);
    throw new Error(
      `Unable to load i-have-adhd rules from ${RULES_PATH}: ${reason}`,
    );
  }

  const rules = content.trim();
  if (!rules) {
    throw new Error(`The i-have-adhd rules file is empty: ${RULES_PATH}`);
  }

  return rules;
}

export default function iHaveAdhdExtension(pi: ExtensionAPI) {
  const rules = loadRules();
  const alwaysOnFlag = join(getAgentDir(), ".i-have-adhd-always");
  const mode = new AdhdMode();

  const updateStatus = (ctx: ExtensionContext, enabled: boolean): void => {
    if (!enabled) {
      ctx.ui.setStatus(STATUS_KEY, undefined);
      return;
    }

    const dot = ctx.ui.theme.fg("success", "●");
    const label = ctx.ui.theme.fg("accent", "ADHD ON");
    ctx.ui.setStatus(STATUS_KEY, `${dot} ${label}`);
  };

  /**
   * Apply the pure state machine's effects to the pi harness. All decisions
   * live in extensions/state-machine.ts; this switch is mechanical glue.
   */
  const applyEffects = (ctx: ExtensionContext, effects: Effect[]): void => {
    for (const effect of effects) {
      switch (effect.kind) {
        case "inject-rules":
          pi.sendMessage(
            {
              customType: RULES_MESSAGE_TYPE,
              content: `${RULES_HEADER}\n\n${rules}`,
              display: false,
            },
            { triggerTurn: false },
          );
          break;
        case "inject-disabled":
          pi.sendMessage(
            {
              customType: DISABLED_MESSAGE_TYPE,
              content: DISABLED_NOTICE,
              display: false,
            },
            { triggerTurn: false },
          );
          break;
        case "persist-state":
          pi.appendEntry(STATE_ENTRY_TYPE, { enabled: effect.enabled });
          break;
        case "set-status":
          updateStatus(ctx, effect.enabled);
          break;
        case "notify":
          ctx.ui.notify(effect.message, "info");
          break;
      }
    }
  };

  /**
   * Keep the conversation in sync with the current mode, the way the Claude Code
   * SessionStart hook does: inject the ruleset once, never per request.
   */
  const syncContext = (ctx: ExtensionContext): void => {
    applyEffects(
      ctx,
      mode.sync(rulesActiveInContext(ctx.sessionManager.buildContextEntries())),
    );
  };

  const restoreState = (ctx: ExtensionContext): void => {
    const savedState = latestEnabledState(ctx.sessionManager.getBranch());
    const enabledByDefault =
      pi.getFlag("adhd") === true || existsSync(alwaysOnFlag);

    applyEffects(
      ctx,
      mode.restore(
        savedState,
        enabledByDefault,
        rulesActiveInContext(ctx.sessionManager.buildContextEntries()),
      ),
    );
  };

  const setEnabled = (nextEnabled: boolean, ctx: ExtensionContext): void => {
    applyEffects(
      ctx,
      mode.setEnabled(
        nextEnabled,
        rulesActiveInContext(ctx.sessionManager.buildContextEntries()),
      ),
    );
  };

  pi.registerFlag("adhd", {
    description: "Start with ADHD-friendly output enabled",
    type: "boolean",
    default: false,
  });

  pi.registerCommand("i-have-adhd", {
    description: "Toggle ADHD-friendly output for this session",
    handler: async (args, ctx) => {
      const argument = args.trim().toLowerCase();

      if (argument === "") {
        setEnabled(!mode.enabled, ctx);
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

      ctx.ui.notify("Usage: /i-have-adhd [on|off]", "warning");
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

    if (mode.enabled && isStopPhrase(input)) {
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
