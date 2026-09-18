// The actual extension runs against an isolated callback host. The only imported
// runtime function, getAgentDir, points to a temporary directory, never user config.
import assert from "node:assert/strict";
import { mkdtempSync, rmSync } from "node:fs";
import { registerHooks } from "node:module";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { after, test } from "node:test";

const agentDir = mkdtempSync(join(tmpdir(), "adhd-lifecycle-"));
const runtimeModule = `export const getAgentDir = () => ${JSON.stringify(agentDir)};`;
const hooks = registerHooks({
  resolve(specifier, context, nextResolve) {
    if (specifier === "@earendil-works/pi-coding-agent") {
      return { url: `data:text/javascript,${encodeURIComponent(runtimeModule)}`, shortCircuit: true };
    }
    if (specifier === "./context-compat") {
      return { url: new URL("../extensions/context-compat.ts", import.meta.url).href,
        format: "module-typescript", shortCircuit: true };
    }
    const resolved = nextResolve(specifier, context);
    return resolved.url.endsWith("/extensions/i-have-adhd.ts")
      ? { ...resolved, format: "module-typescript" } : resolved;
  },
});
const { default: initialize } = await import("../extensions/i-have-adhd.ts");
after(() => {
  hooks.deregister();
  rmSync(agentDir, { recursive: true, force: true });
});

const saved = (enabled) => ({
  type: "custom", customType: "i-have-adhd-state", data: { enabled },
});
const rules = { customType: "i-have-adhd-rules", content: "Saved rules", display: false };

function host({ runtime = "omp", defaultOn = false } = {}) {
  const handlers = new Map();
  const commands = new Map();
  let branch = [];
  let messages = [];
  let status;
  const manager = { getBranch: () => branch };
  if (runtime === "omp") {
    manager.buildSessionContext = () => ({ messages });
  } else {
    manager.buildContextEntries = () => messages;
  }
  const ctx = {
    hasUI: true, sessionManager: manager,
    ui: {
      theme: { fg: (_color, text) => text },
      setStatus: (_key, text) => { status = text; }, notify() {},
    },
  };
  const inContext = (message) => runtime === "omp"
    ? { role: "custom", ...message }
    : { type: "custom_message", ...message };
  initialize({
    registerFlag() {}, getFlag: () => defaultOn,
    registerCommand: (name, command) => commands.set(name, command),
    on: (name, handler) => handlers.set(name, handler),
    appendEntry: (customType, data) => branch.push({ type: "custom", customType, data }),
    sendMessage: (message, options) => {
      assert.equal(options.triggerTurn, false, "state restoration must not start a model turn");
      messages.push(inContext(message));
    },
  });
  return {
    emit: async (name, event = {}) => handlers.get(name)?.({ type: name, ...event }, ctx),
    command: (args) => commands.get("i-have-adhd").handler(args, ctx),
    replace: (entries = [], context = []) => { branch = [...entries]; messages = context.map(inContext); },
    compact: async () => { messages = []; await handlers.get("session_compact")?.({}, ctx); },
    snapshot: () => ({ status, states: branch.map((entry) => entry.data.enabled),
      markers: messages.map((message) => message.customType) }),
  };
}

test("OMP new session restores default off before compaction", async () => {
  const h = host();
  await h.emit("session_start");
  await h.command("on");
  h.replace();
  await h.emit("session_switch", { reason: "new" });
  assert.equal(h.snapshot().status, undefined);
  await h.compact();
  assert.deepEqual(h.snapshot().markers, []);
});

test("OMP resume restores saved off even with an enabled default", async () => {
  const h = host({ defaultOn: true });
  await h.emit("session_start");
  h.replace([saved(false)]);
  await h.emit("session_switch", { reason: "resume", previousSessionFile: "/prior.jsonl" });
  assert.equal(h.snapshot().status, undefined);
  await h.compact();
  assert.deepEqual(h.snapshot().markers, []);
});

test("OMP fork into saved off cancels a stale rules marker exactly once", async () => {
  const h = host();
  await h.emit("session_start");
  await h.command("on");
  h.replace([saved(false)], [rules]);
  await h.emit("session_switch", { reason: "fork", previousSessionFile: "/prior.jsonl" });
  await h.emit("session_switch", { reason: "fork", previousSessionFile: "/prior.jsonl" });
  assert.equal(h.snapshot().status, undefined);
  assert.deepEqual(h.snapshot().markers, ["i-have-adhd-rules", "i-have-adhd-disabled"]);
  await h.compact();
  assert.deepEqual(h.snapshot().markers, []);
});

test("OMP branch toggle flips the destination's saved disabled state", async () => {
  const h = host();
  await h.emit("session_start");
  await h.command("on");
  h.replace([saved(false)]);
  await h.emit("session_branch", { previousSessionFile: "/prior.jsonl" });
  await h.command("");
  assert.deepEqual(h.snapshot().states, [false, true]);
  assert.match(h.snapshot().status, /ADHD ON/);
  assert.deepEqual(h.snapshot().markers, ["i-have-adhd-rules"]);
});

test("OMP enabled destination restores status without duplicating its active rules", async () => {
  const h = host();
  await h.emit("session_start");
  h.replace([saved(true)], [rules]);
  await h.emit("session_switch", { reason: "resume" });
  await h.emit("session_switch", { reason: "resume" });
  assert.match(h.snapshot().status, /ADHD ON/);
  assert.deepEqual(h.snapshot().markers, ["i-have-adhd-rules"]);
  await h.compact();
  assert.deepEqual(h.snapshot().markers, ["i-have-adhd-rules"]);
});

test("OMP fresh destination applies the startup flag after leaving a disabled session", async () => {
  const h = host({ defaultOn: true });
  await h.emit("session_start");
  await h.command("off");
  h.replace();
  await h.emit("session_switch", { reason: "new" });
  assert.match(h.snapshot().status, /ADHD ON/);
  assert.deepEqual(h.snapshot().markers, ["i-have-adhd-rules"]);
});

test("Pi start/tree, compaction, skill alias, and stop controls remain compatible", async () => {
  const h = host({ runtime: "pi" });
  h.replace([saved(true)], [rules]);
  await h.emit("session_start");
  assert.match(h.snapshot().status, /ADHD ON/);
  assert.deepEqual(h.snapshot().markers, ["i-have-adhd-rules"]);
  h.replace([saved(false)], [rules]);
  await h.emit("session_tree");
  assert.equal(h.snapshot().status, undefined);
  assert.deepEqual(h.snapshot().markers, ["i-have-adhd-rules", "i-have-adhd-disabled"]);
  await h.compact();
  assert.deepEqual(h.snapshot().markers, []);
  assert.deepEqual(await h.emit("input", { text: "/skill:i-have-adhd" }), { action: "handled" });
  assert.deepEqual(h.snapshot().markers, ["i-have-adhd-rules"]);
  assert.deepEqual(await h.emit("input", { text: "normal mode" }), { action: "handled" });
  assert.equal(h.snapshot().status, undefined);
  assert.deepEqual(await h.emit("input", { text: "normal mode" }), { action: "continue" });
});
