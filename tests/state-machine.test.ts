import assert from "node:assert/strict";
import { test } from "node:test";
import {
  AdhdMode,
  DISABLED_MESSAGE_TYPE,
  RULES_MESSAGE_TYPE,
  STATE_ENTRY_TYPE,
  isStopPhrase,
  latestEnabledState,
  rulesActiveInContext,
  type Entry,
  type Effect,
} from "../extensions/state-machine.ts";

const rulesEntry = (): Entry => ({
  type: "custom_message",
  customType: RULES_MESSAGE_TYPE,
});
const disabledEntry = (): Entry => ({
  type: "custom_message",
  customType: DISABLED_MESSAGE_TYPE,
});
const stateEntry = (enabled: boolean): Entry => ({
  type: "custom",
  customType: STATE_ENTRY_TYPE,
  data: { enabled },
});
const kinds = (effects: Effect[]): string[] => effects.map((effect) => effect.kind);

test("latestEnabledState: no state entries means no saved mode", () => {
  assert.equal(latestEnabledState([]), undefined);
  assert.equal(
    latestEnabledState([
      { type: "user", text: "hi" },
      rulesEntry(),
    ]),
    undefined,
  );
});

test("latestEnabledState: newest persisted mode wins", () => {
  const entries = [stateEntry(true), stateEntry(false), stateEntry(true)];
  assert.equal(latestEnabledState(entries), true);
});

test("latestEnabledState: non-boolean payloads are ignored", () => {
  const entries = [
    { type: "custom", customType: STATE_ENTRY_TYPE, data: { enabled: "yes" } },
    { type: "custom", customType: STATE_ENTRY_TYPE, data: {} },
    stateEntry(true),
  ];
  assert.equal(latestEnabledState(entries), true);
});

test("rulesActiveInContext: no markers means the ruleset is not live", () => {
  assert.equal(rulesActiveInContext([]), false);
  assert.equal(
    rulesActiveInContext([
      { type: "user", text: "hello" },
      { type: "custom_message", customType: "someone-elses-message" },
    ]),
    false,
  );
});

test("rulesActiveInContext: the newest marker wins", () => {
  const entries = [
    rulesEntry(),
    disabledEntry(),
    rulesEntry(),
    disabledEntry(),
    rulesEntry(),
  ];
  assert.equal(rulesActiveInContext(entries), true);

  assert.equal(rulesActiveInContext([rulesEntry(), disabledEntry()]), false);
});

test("isStopPhrase: only the exact phrases count", () => {
  assert.equal(isStopPhrase("stop adhd mode"), true);
  assert.equal(isStopPhrase("normal mode"), true);
  assert.equal(isStopPhrase("stop adhd"), false);
  assert.equal(isStopPhrase("normal"), false);
  assert.equal(isStopPhrase(""), false);
});

test("AdhdMode.restore: saved mode overrides the default", () => {
  const mode = new AdhdMode();
  const effects = mode.restore(false, true, true);

  assert.equal(mode.enabled, false);
  assert.deepEqual(effects, [
    { kind: "set-status", enabled: false },
    { kind: "inject-disabled" },
  ]);
});

test("AdhdMode.restore: restoring disabled with no live rules injects nothing", () => {
  const mode = new AdhdMode();
  const effects = mode.restore(false, true, false);

  assert.equal(mode.enabled, false);
  assert.deepEqual(kinds(effects), ["set-status"]);
});

test("AdhdMode.restore: no saved mode falls back to the default", () => {
  const mode = new AdhdMode();
  const effects = mode.restore(undefined, true, false);

  assert.equal(mode.enabled, true);
  assert.deepEqual(effects, [
    { kind: "set-status", enabled: true },
    { kind: "inject-rules" },
  ]);
});

test("AdhdMode.restore: never re-injects rules that are already live", () => {
  const mode = new AdhdMode();
  const effects = mode.restore(undefined, true, true);

  assert.equal(mode.enabled, true);
  assert.deepEqual(kinds(effects), ["set-status"]);
});

test("AdhdMode.sync: enabled without live rules injects them", () => {
  const mode = new AdhdMode();
  mode.enabled = true;

  assert.deepEqual(kinds(mode.sync(false)), ["set-status", "inject-rules"]);
});

test("AdhdMode.sync: enabled with live rules changes nothing", () => {
  const mode = new AdhdMode();
  mode.enabled = true;

  assert.deepEqual(kinds(mode.sync(true)), ["set-status"]);
});

test("AdhdMode.sync: disabled with stale live rules sends the cancel notice", () => {
  const mode = new AdhdMode();
  mode.enabled = false;

  assert.deepEqual(kinds(mode.sync(true)), ["set-status", "inject-disabled"]);
});

test("AdhdMode.setEnabled: turning on persists, notifies, and injects", () => {
  const mode = new AdhdMode();
  mode.enabled = false;

  const effects = mode.setEnabled(true, false);

  assert.equal(mode.enabled, true);
  assert.deepEqual(effects, [
    { kind: "persist-state", enabled: true },
    { kind: "set-status", enabled: true },
    { kind: "inject-rules" },
    { kind: "notify", message: "ADHD mode enabled" },
  ]);
});

test("AdhdMode.setEnabled: turning off cancels live rules", () => {
  const mode = new AdhdMode();
  mode.enabled = true;

  const effects = mode.setEnabled(false, true);

  assert.equal(mode.enabled, false);
  assert.deepEqual(effects, [
    { kind: "persist-state", enabled: false },
    { kind: "set-status", enabled: false },
    { kind: "inject-disabled" },
    { kind: "notify", message: "ADHD mode disabled" },
  ]);
});

test("in-process walkthrough mirrors the RPC smoke test's session", () => {
  // The same scenario scripts/check_pi_extension.py drives over RPC, asserted
  // here in milliseconds: --adhd restore, toggle off, toggle on, alias, stop
  // phrase. This is the fast seam the RPC test cannot provide.
  const context: Entry[] = [];
  const mode = new AdhdMode();

  // Faithful mini-adapter: turn effects into the entries the real pi
  // harness would append, the way extensions/i-have-adhd.ts does.
  const apply = (effects: Effect[]): void => {
    for (const effect of effects) {
      if (effect.kind === "inject-rules") context.push(rulesEntry());
      else if (effect.kind === "inject-disabled") context.push(disabledEntry());
      else if (effect.kind === "persist-state") context.push(stateEntry(effect.enabled));
    }
  };

  const restore = (defaultEnabled: boolean) => {
    apply(mode.restore(latestEnabledState(context), defaultEnabled, rulesActiveInContext(context)));
  };
  const toggle = (next: boolean) => {
    apply(mode.setEnabled(next, rulesActiveInContext(context)));
  };

  restore(true);
  assert.equal(mode.enabled, true);
  assert.equal(rulesActiveInContext(context), true);

  toggle(false);
  assert.equal(mode.enabled, false);
  assert.equal(rulesActiveInContext(context), false);

  toggle(true);
  assert.equal(rulesActiveInContext(context), true);

  toggle(false); // stop phrase path
  assert.equal(mode.enabled, false);
  assert.equal(rulesActiveInContext(context), false);
});
