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
  let liveMessages = [];
  let preparing = false;
  const queuedMessages = [];
  const sends = [];
  let status;
  const manager = { getBranch: () => branch };
  if (runtime === "omp") {
    manager.buildSessionContext = () => ({ messages: [...messages] });
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
  const persist = (message) => {
    const entry = inContext(message);
    messages.push(entry);
    liveMessages.push(entry);
  };
  const flush = async () => { await Promise.all(sends.splice(0)); };
  const compact = async () => {
    messages = [];
    liveMessages = [];
    await handlers.get("session_compact")?.({}, ctx);
    await flush();
  };
  initialize({
    registerFlag() {}, getFlag: () => defaultOn,
    registerCommand: (name, command) => commands.set(name, command),
    on: (name, handler) => handlers.set(name, handler),
    appendEntry: (customType, data) => branch.push({ type: "custom", customType, data }),
    sendMessage: (message, options) => {
      assert.equal(options.triggerTurn, false, "state restoration must not start a model turn");
      // OMP normalizes sent messages asynchronously. During prompt preparation,
      // sendMessage queues steering instead of adding to this prompt's context.
      sends.push(Promise.resolve().then(() => {
        if (preparing) queuedMessages.push(message);
        else persist(message);
      }));
    },
  });
  return {
    emit: async (name, event = {}) => {
      // OMP resume/branch restore a context snapshot captured BEFORE handlers.
      // A message sent inside the handler persists but is absent from live state.
      // See agent-session.ts at e1a86ce4f962d5e06e05270d2a48f71608feab30:
      // switchSession (9595-9610), branch (9915-9926).
      const restoresSnapshot = runtime === "omp" && (name === "session_branch"
        || (name === "session_switch" && event.reason === "resume"));
      const snapshot = [...messages];
      const result = await handlers.get(name)?.({ type: name, ...event }, ctx);
      await flush();
      if (restoresSnapshot) liveMessages = snapshot;
      return result;
    },
    command: async (args) => {
      await commands.get("i-have-adhd").handler(args, ctx);
      await flush();
    },
    replace: (entries = [], context = []) => {
      branch = [...entries];
      messages = context.map(inContext);
      liveMessages = [...messages];
    },
    compact,
    startAgent: async ({ commit = true, compactAfterPrepare = false } = {}) => {
      preparing = true;
      const result = await handlers.get("before_agent_start")?.({
        type: "before_agent_start", prompt: "Next task", images: undefined, systemPrompt: [],
      }, ctx);
      await flush();
      if (compactAfterPrepare) await compact();
      // The supported returned-message contract joins the prompt after restore
      // and persists on delivery; abandoned preparation must not consume it.
      if (commit && result?.message) persist(result.message);
      preparing = false;
      return result;
    },
    snapshot: () => ({ status, states: branch.map((entry) => entry.data.enabled),
      markers: messages.map((message) => message.customType),
      liveMarkers: liveMessages.map((message) => message.customType),
      queuedMarkers: queuedMessages.map((message) => message.customType) }),
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
  await h.startAgent();
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
  await h.startAgent();
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
  await h.startAgent();
  assert.deepEqual(h.snapshot().markers, ["i-have-adhd-rules"]);
});

for (const event of ["session_switch", "session_branch"]) {
  test(`OMP ${event} delivers missing rules to the first live prompt once`, async () => {
    const h = host({ defaultOn: true });
    await h.emit("session_start");
    h.replace();
    await h.emit(event, { reason: "resume" });
    assert.match(h.snapshot().status, /ADHD ON/);
    await h.startAgent();
    assert.deepEqual(h.snapshot().liveMarkers, ["i-have-adhd-rules"]);
    await h.startAgent();
    assert.deepEqual(h.snapshot().markers, ["i-have-adhd-rules"]);
    assert.deepEqual(h.snapshot().liveMarkers, ["i-have-adhd-rules"]);
    assert.deepEqual(h.snapshot().queuedMarkers, []);
  });

  test(`OMP ${event} cancels stale rules in the live prompt when saved off`, async () => {
    const h = host({ defaultOn: true });
    await h.emit("session_start");
    h.replace([saved(false)], [rules]);
    await h.emit(event, { reason: "resume" });
    assert.equal(h.snapshot().status, undefined);
    await h.startAgent();
    assert.deepEqual(h.snapshot().liveMarkers, ["i-have-adhd-rules", "i-have-adhd-disabled"]);
    await h.startAgent();
    assert.deepEqual(h.snapshot().markers, ["i-have-adhd-rules", "i-have-adhd-disabled"]);
    assert.deepEqual(h.snapshot().queuedMarkers, []);
  });
}

test("OMP abandoned prompt preparation retains pending rules for the next delivery", async () => {
  const h = host({ defaultOn: true });
  await h.emit("session_start");
  h.replace();
  await h.emit("session_switch", { reason: "resume" });
  await h.startAgent({ commit: false });
  assert.deepEqual(h.snapshot().markers, []);
  await h.startAgent();
  assert.deepEqual(h.snapshot().liveMarkers, ["i-have-adhd-rules"]);
});

test("OMP compaction during pending preparation does not queue duplicate rules", async () => {
  const h = host({ defaultOn: true });
  await h.emit("session_start");
  h.replace();
  await h.emit("session_switch", { reason: "resume" });
  await h.startAgent({ compactAfterPrepare: true });
  assert.deepEqual(h.snapshot().queuedMarkers, []);
  assert.deepEqual(h.snapshot().liveMarkers, ["i-have-adhd-rules"]);
  await h.startAgent();
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
