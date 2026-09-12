import { createHash } from "node:crypto";
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
  latestMarkerContent,
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
const DISABLED_NOTICE =
  "ADHD MODE OFF. Ignore the i-have-adhd ruleset injected earlier in this conversation and return to your default response style.";

// Matches the [i-have-adhd:<hash>] tag embedded in an injected ruleset
// message, so a later check can tell a still-current injection from a stale
// one (SKILL.md changed after it was injected -- e.g. the plugin was
// upgraded mid-session). Content-derived, not a semantic version: it exists
// to detect drift, not to be read as a release number.
function rulesTag(hash: string): string {
  return `[i-have-adhd:${hash}]`;
}

function hashRules(rules: string): string {
  return createHash("sha256").update(rules, "utf8").digest("hex").slice(0, 12);
}

function rulesHeader(hash: string): string {
  return (
    'ADHD MODE ACTIVE. The ruleset below applies to every response until turned off. ' +
    '"stop adhd mode" or "normal mode" turns it off for this session. ' +
    rulesTag(hash)
  );
}

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
  // `null` (as opposed to the key being absent) marks an explicit reset --
  // see getSavedState and setEnabled.
  mode?: ResponseMode | null;
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
  let enabledState: boolean | undefined;
  let modeState: ResponseMode | undefined;

  for (const entry of ctx.sessionManager.getBranch()) {
    if (entry.type !== "custom" || entry.customType !== STATE_ENTRY_TYPE) {
      continue;
    }

    const data = entry.data as { enabled?: unknown; mode?: unknown } | undefined;
    if (typeof data?.enabled !== "boolean") continue;
    enabledState = data.enabled;

    // Three cases for `mode` on a given entry:
    //  - a real mode string: adopt it.
    //  - `null`: an explicit reset (written when turning off -- see
    //    setEnabled), distinct from the key being absent. Clears the
    //    carried-forward value instead of leaving it untouched.
    //  - absent (older entries written before mode support existed, or an
    //    entry that only toggled `enabled`): carry the previous value
    //    forward, so a mode chosen earlier in the branch survives a later
    //    on/off toggle that doesn't itself mention mode.
    if (data.mode === null) {
      modeState = undefined;
    } else if (isResponseMode(data.mode)) {
      modeState = data.mode;
    }
  }

  return enabledState === undefined
    ? undefined
    : { enabled: enabledState, mode: modeState };
}

/**
 * The content of the latest active i-have-adhd-rules marker, or `undefined`
 * if none is active (never injected, or cancelled by a later disabled
 * notice). The one place both checks below read from, so they can't
 * silently diverge on how a message is found even if one grows a different
 * final condition than the other.
 */
function latestRulesContent(ctx: ExtensionContext): string | undefined {
  return latestMarkerContent(
    contextMessages(ctx.sessionManager),
    RULES_MESSAGE_TYPE,
    DISABLED_MESSAGE_TYPE,
  );
}

/**
 * Whether the CURRENT ruleset (matching `expectedHash`) is still live in the
 * context the model actually receives.
 *
 * Beyond presence, the embedded tag has to match `expectedHash` too -- a
 * present-but-stale injection (SKILL.md changed since it went in, e.g. an
 * upgrade mid-session) is treated the same as "not injected," so the caller
 * replaces it instead of leaving the model on an outdated ruleset for the
 * rest of the session. If content isn't available on this API surface at
 * all, latestRulesContent already reports that as `undefined`, and
 * undefined content fails the hash check the same way -- fails toward
 * re-injecting, not toward silently trusting stale text.
 */
function rulesAreCurrentInContext(
  ctx: ExtensionContext,
  expectedHash: string,
): boolean {
  const content = latestRulesContent(ctx);
  return content !== undefined && content.includes(rulesTag(expectedHash));
}

/**
 * Presence only, ignoring currency: some ruleset (current or stale) is the
 * active marker. Deliberately separate from rulesAreCurrentInContext -- the
 * "should I cancel what's there with a disabled notice" decision cares that
 * *something* is visible to the model, not whether it happens to be the
 * latest revision. Using the currency-aware check there instead would skip
 * the disabled notice for a stale-but-present ruleset, leaving the model
 * quietly following rules the reader just turned off.
 */
function rulesAreInContext(ctx: ExtensionContext): boolean {
  return latestRulesContent(ctx) !== undefined;
}

export default function iHaveAdhdExtension(pi: ExtensionAPI) {
  const rules = loadRules();
  const rulesHash = hashRules(rules);
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
    const current = rulesAreCurrentInContext(ctx, rulesHash);

    if (enabled && !current) {
      // Covers both "never injected this session" and "injected, but
      // SKILL.md changed since (a stale hash) -- e.g. the plugin was
      // upgraded mid-session" the same way: a fresh injection with the
      // current content. Fold the active response mode into the same
      // injection instead of a separate marker: this is the one point
      // where the ruleset (and so the mode) has to survive compaction, so
      // there is nothing extra to keep synchronized after this.
      const modeNote = mode ? `\n\n${modeDirective(mode)}` : "";
      pi.sendMessage(
        {
          customType: RULES_MESSAGE_TYPE,
          content: `${rulesHeader(rulesHash)}\n\n${rules}${modeNote}`,
          display: false,
        },
        { triggerTurn: false },
      );
      return;
    }

    if (!enabled && rulesAreInContext(ctx)) {
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
    // A hard off promises "return to your default response style" (see
    // DISABLED_NOTICE): a mode pinned before turning off must not silently
    // resurrect on the next enable. `null` (not just leaving the key off
    // the entry) marks this as an explicit reset -- see getSavedState.
    if (!enabled) mode = undefined;
    pi.appendEntry(STATE_ENTRY_TYPE, {
      enabled,
      mode: enabled ? mode : null,
    } satisfies AdhdModeState);
    updateStatus(ctx);
    syncContext(ctx);
    ctx.ui.notify(`ADHD mode ${enabled ? "enabled" : "disabled"}`, "info");
  };

  const setMode = (nextMode: ResponseMode, ctx: ExtensionContext): void => {
    // Capture this before syncContext can change it: if the current rules
    // aren't in context yet (missing, or present but stale -- see
    // rulesAreCurrentInContext), syncContext below injects them fresh with
    // the new mode already folded in, and this check would then read back
    // `true` against that fresh injection -- sending a second, redundant
    // standalone message on top of it.
    const rulesAlreadyCurrent = rulesAreCurrentInContext(ctx, rulesHash);

    mode = nextMode;
    // Setting a mode implies wanting the ruleset active; a mode with the
    // ruleset off would have nothing to modify.
    enabled = true;
    pi.appendEntry(STATE_ENTRY_TYPE, { enabled, mode } satisfies AdhdModeState);
    updateStatus(ctx);
    syncContext(ctx);

    // If the current rules were already in context, syncContext above does
    // nothing (it only (re-)injects when missing or stale) -- send the mode
    // change on its own so the model sees it without waiting for the next
    // compaction-triggered re-injection.
    if (rulesAlreadyCurrent) {
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
