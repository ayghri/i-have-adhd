/**
 * Pure state machine for the i-have-adhd extension.
 *
 * Deliberately imports nothing from pi or node: every decision the extension
 * makes about mode, injection, and persistence lives here, so it can be
 * exercised in-process with `node --test` (see tests/state-machine.test.ts)
 * without booting the pi harness or having pi installed. The extension in
 * i-have-adhd.ts stays a thin executor that applies the effects.
 */

export const STATE_ENTRY_TYPE = "i-have-adhd-state";
export const RULES_MESSAGE_TYPE = "i-have-adhd-rules";
export const DISABLED_MESSAGE_TYPE = "i-have-adhd-disabled";

export const STOP_PHRASES = new Set(["stop adhd mode", "normal mode"]);

export type Entry = {
  type: string;
  customType?: string;
  data?: unknown;
};

export function isStopPhrase(input: string): boolean {
  return STOP_PHRASES.has(input);
}

/** Newest persisted mode wins; entries with a non-boolean payload are ignored. */
export function latestEnabledState(entries: readonly Entry[]): boolean | undefined {
  let saved: boolean | undefined;

  for (const entry of entries) {
    if (entry.type !== "custom" || entry.customType !== STATE_ENTRY_TYPE) {
      continue;
    }
    const data = entry.data as { enabled?: unknown } | undefined;
    if (typeof data?.enabled === "boolean") {
      saved = data.enabled;
    }
  }

  return saved;
}

/**
 * Whether the rules are still live in the context the model actually receives.
 *
 * Only the newest marker counts: a later "disabled" notice cancels an earlier
 * ruleset, and compaction drops summarized entries so the ruleset has to be
 * injected again.
 */
export function rulesActiveInContext(entries: readonly Entry[]): boolean {
  let active = false;

  for (const entry of entries) {
    if (entry.type !== "custom_message") continue;

    if (entry.customType === RULES_MESSAGE_TYPE) {
      active = true;
    } else if (entry.customType === DISABLED_MESSAGE_TYPE) {
      active = false;
    }
  }

  return active;
}

export type Effect =
  | { kind: "inject-rules" }
  | { kind: "inject-disabled" }
  | { kind: "persist-state"; enabled: boolean }
  | { kind: "set-status"; enabled: boolean }
  | { kind: "notify"; message: string };

/**
 * The session's mode plus the effects each transition must have, so the pi
 * adapter stays a thin executor and every decision is testable in isolation.
 */
export class AdhdMode {
  enabled: boolean = false;

  /** Restore the saved mode (or the default) and bring the context in sync. */
  restore(
    saved: boolean | undefined,
    enabledByDefault: boolean,
    rulesActive: boolean,
  ): Effect[] {
    this.enabled = saved ?? enabledByDefault;
    return this.sync(rulesActive);
  }

  /** Reconcile the context with the current mode, e.g. after compaction. */
  sync(rulesActive: boolean): Effect[] {
    const effects: Effect[] = [{ kind: "set-status", enabled: this.enabled }];

    if (this.enabled && !rulesActive) {
      effects.push({ kind: "inject-rules" });
    } else if (!this.enabled && rulesActive) {
      effects.push({ kind: "inject-disabled" });
    }

    return effects;
  }

  /** Toggle the mode on or off, persisting the change and syncing the context. */
  setEnabled(next: boolean, rulesActive: boolean): Effect[] {
    this.enabled = next;
    return [
      { kind: "persist-state", enabled: next },
      ...this.sync(rulesActive),
      { kind: "notify", message: `ADHD mode ${next ? "enabled" : "disabled"}` },
    ];
  }
}
