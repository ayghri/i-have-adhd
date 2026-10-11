import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import { homedir } from "node:os";
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

// Matches the "explain_reasoning" values documented in the skill's
// "Preferences (optional)" section.
const EXPLAIN_REASONING_LEVELS = ["minimal", "normal", "detailed"] as const;
type ExplainReasoning = (typeof EXPLAIN_REASONING_LEVELS)[number];

function isExplainReasoning(value: unknown): value is ExplainReasoning {
  return (
    typeof value === "string" &&
    (EXPLAIN_REASONING_LEVELS as readonly string[]).includes(value)
  );
}

const PREFERENCES_FILENAME = ".i-have-adhd.json";

// Mirrors the schema documented in the skill's "Preferences (optional)"
// section -- keep the two in sync if this shape changes. Every field is
// optional and validated independently in parsePreferencesJson: one invalid
// or misspelled field is dropped on its own rather than rejecting the whole
// file, so a typo in `show_estimates` doesn't also silently disable
// `max_steps`.
type AdhdPreferences = {
  maxSteps?: number;
  showCompleted?: boolean;
  showBlockers?: boolean;
  showEstimates?: boolean;
  explainReasoning?: ExplainReasoning;
  requireVerification?: boolean;
  showChangedFiles?: boolean;
};

type UserPreferences = {
  // "adaptive" (or the field absent/invalid) is not a real ResponseMode --
  // it means "keep the automatic classifier," so it collapses to undefined
  // here rather than being carried around as a fifth mode value.
  mode?: ResponseMode;
  prefs: AdhdPreferences;
};

function readBoolean(value: unknown): boolean | undefined {
  return typeof value === "boolean" ? value : undefined;
}

function parsePreferencesJson(raw: unknown): UserPreferences {
  const empty: UserPreferences = { prefs: {} };
  if (raw === null || typeof raw !== "object") return empty;

  const root = raw as Record<string, unknown>;
  const mode = isResponseMode(root.mode) ? root.mode : undefined;

  const prefs: AdhdPreferences = {};
  const preferences = root.preferences;
  if (preferences !== null && typeof preferences === "object") {
    const p = preferences as Record<string, unknown>;

    if (
      typeof p.max_steps === "number" &&
      Number.isInteger(p.max_steps) &&
      p.max_steps >= 1 &&
      p.max_steps <= 20
    ) {
      prefs.maxSteps = p.max_steps;
    }

    const showCompleted = readBoolean(p.show_completed);
    if (showCompleted !== undefined) prefs.showCompleted = showCompleted;

    const showBlockers = readBoolean(p.show_blockers);
    if (showBlockers !== undefined) prefs.showBlockers = showBlockers;

    const showEstimates = readBoolean(p.show_estimates);
    if (showEstimates !== undefined) prefs.showEstimates = showEstimates;

    if (isExplainReasoning(p.explain_reasoning)) {
      prefs.explainReasoning = p.explain_reasoning;
    }
  }

  const coding = root.coding;
  if (coding !== null && typeof coding === "object") {
    const c = coding as Record<string, unknown>;

    const requireVerification = readBoolean(c.require_verification);
    if (requireVerification !== undefined) {
      prefs.requireVerification = requireVerification;
    }

    const showChangedFiles = readBoolean(c.show_changed_files);
    if (showChangedFiles !== undefined) {
      prefs.showChangedFiles = showChangedFiles;
    }
  }

  return { mode, prefs };
}

/**
 * Loads the reader's own preferences -- distinct from `loadConfig`'s
 * `i-have-adhd.json` in the Pi agent dir, which holds harness-level settings
 * (`alwaysOn`, `hideStatus`) rather than reader-facing ones. This file lives
 * where the reader actually works, following the same lookup and schema
 * documented in SKILL.md's "Preferences (optional)" section, so a prompt-only
 * runtime with no extension code (Claude Code, Codex, ...) can honor the
 * identical file just by reading it when instructed to.
 *
 * A project-level file wins over a home-directory one when both exist, so a
 * personal default (home) can be overridden per-project without editing it.
 * Missing, unreadable, or invalid JSON all fail open to "no preferences"
 * rather than blocking startup -- the same failure direction as `loadConfig`
 * and `contextMessages` elsewhere in this file.
 *
 * A project-level file that parses but has no valid fields (every key typo'd
 * or wrongly typed) is NOT treated as a parse failure: it does not fall
 * through to the home-directory file. That file did exist and was read --
 * silently substituting a different file's settings for it would be more
 * surprising than the reader getting no overrides and being able to see
 * their own file has no valid fields in it.
 */
function loadUserPreferences(): UserPreferences {
  const candidates = [
    join(process.cwd(), PREFERENCES_FILENAME),
    join(homedir(), PREFERENCES_FILENAME),
  ];

  for (const path of candidates) {
    try {
      if (!existsSync(path)) continue;
      return parsePreferencesJson(JSON.parse(readFileSync(path, "utf8")));
    } catch {
      continue;
    }
  }

  return { prefs: {} };
}

/**
 * A directive block folded into the ruleset injection, the same way
 * modeDirective is. Only preferences that actually change behavior from the
 * documented defaults produce a line -- e.g. `showChangedFiles` is opt-in, so
 * only `true` is worth stating; `showEstimates` is on by default, so only
 * `false` is. Returns undefined (add nothing) when no preference deviates
 * from default, so a reader with no preferences file sees no extra text.
 */
function preferencesDirective(prefs: AdhdPreferences): string | undefined {
  const lines: string[] = [];

  if (prefs.maxSteps !== undefined) {
    lines.push(
      `- Cap numbered steps (rule 2) at ${prefs.maxSteps}; never inflate a shorter plan to reach it.`,
    );
  }
  if (prefs.showCompleted === false) {
    lines.push(
      "- Omit the Task State Completed field even when it has content.",
    );
  }
  if (prefs.showBlockers === false) {
    lines.push(
      "- Omit the Task State Blockers field even when it has content.",
    );
  }
  if (prefs.showEstimates === false) {
    lines.push("- Skip rule 6 (time estimates) for the rest of this session.");
  }
  if (prefs.explainReasoning === "minimal") {
    lines.push(
      "- Keep reasoning at compact mode's tightness regardless of the active Response Mode.",
    );
  } else if (prefs.explainReasoning === "detailed") {
    lines.push(
      '- Apply "When to break the rules" item 1 (explain fully) by default, without waiting to be asked.',
    );
  }
  if (prefs.requireVerification === false) {
    lines.push(
      "- Verification-First still applies whenever a check is possible; when none is, state that once if relevant instead of calling it out every turn.",
    );
  }
  if (prefs.showChangedFiles === true) {
    lines.push(
      "- Rule 7 (make completed work visible): list the changed files for code changes.",
    );
  }

  if (lines.length === 0) return undefined;

  return (
    `User preferences (from ${PREFERENCES_FILENAME}) apply for this session, ` +
    "unless Priority's safety/correctness rule requires otherwise:\n" +
    lines.join("\n")
  );
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
  // Loaded once at startup, like `config` above: preferences shape the
  // ruleset text injected at session start, not a live runtime toggle, so
  // there is no reload-preferences command to keep in sync with a later edit
  // of the file (edit it, then start a new session to pick it up).
  const userPreferences = loadUserPreferences();
  const prefsNote = preferencesDirective(userPreferences.prefs);
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
      const preferencesNote = prefsNote ? `\n\n${prefsNote}` : "";
      pi.sendMessage(
        {
          customType: RULES_MESSAGE_TYPE,
          content: `${rulesHeader(rulesHash)}\n\n${rules}${modeNote}${preferencesNote}`,
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
    // A pinned mode from the preferences file only seeds a session that has
    // never saved any state of its own -- once the reader has toggled
    // enabled/mode at all this session (even to explicitly reset the mode
    // via a hard off, which saves `mode: null`), that saved state wins, the
    // same way `enabledByDefault` only applies absent a saved `enabled`.
    mode = savedState ? savedState.mode : userPreferences.mode;
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
