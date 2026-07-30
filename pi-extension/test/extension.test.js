import assert from "node:assert/strict";
import { mkdtempSync, rmSync, writeFileSync, mkdirSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import adhdExtension, {
  isDeactivationCommand,
  stripFrontmatter,
} from "../index.js";

// -- Test harness --

function createPiHarness() {
  const events = new Map();
  const commands = new Map();
  const appendedEntries = [];
  const sentUserMessages = [];

  const pi = {
    on(eventName, handler) {
      events.set(eventName, handler);
    },
    registerCommand(name, options) {
      commands.set(name, options);
    },
    appendEntry(customType, data) {
      appendedEntries.push({ customType, data });
    },
    sendUserMessage(text, options) {
      sentUserMessages.push({ text, options });
    },
  };

  adhdExtension(pi);
  return { events, commands, appendedEntries, sentUserMessages };
}

function createCommandContext(overrides = {}) {
  return {
    isIdle: () => true,
    sessionManager: { getEntries: () => [] },
    ui: { notify() {} },
    ...overrides,
  };
}

function withTempHome(fn) {
  const tempHome = mkdtempSync(join(tmpdir(), "adhd-test-"));
  const previousHome = process.env.HOME;
  const previousAlways = process.env.I_HAVE_ADHD_ALWAYS;
  process.env.HOME = tempHome;
  delete process.env.I_HAVE_ADHD_ALWAYS;

  return Promise.resolve()
    .then(() => fn(tempHome))
    .finally(() => {
      if (previousHome === undefined) delete process.env.HOME;
      else process.env.HOME = previousHome;
      if (previousAlways === undefined) delete process.env.I_HAVE_ADHD_ALWAYS;
      else process.env.I_HAVE_ADHD_ALWAYS = previousAlways;
      rmSync(tempHome, { recursive: true, force: true });
    });
}

// -- Tests --

test("extension registers /i-have-adhd command", () => {
  const { commands } = createPiHarness();
  assert.deepEqual([...commands.keys()], ["i-have-adhd"]);
});

test("/i-have-adhd activates and injects instructions", async () => {
  await withTempHome(async () => {
    const { commands, events, appendedEntries } = createPiHarness();
    const ctx = createCommandContext();

    // session_start with no flag file → inactive
    await events.get("session_start")({}, ctx);
    const beforeOff = await events.get("before_agent_start")(
      { systemPrompt: "BASE" },
      ctx,
    );
    assert.equal(beforeOff, undefined);

    // Turn on
    await commands.get("i-have-adhd").handler("", ctx);
    assert.deepEqual(appendedEntries.at(-1), {
      customType: "adhd-mode",
      data: { active: true },
    });

    // Should now inject into system prompt
    const result = await events.get("before_agent_start")(
      { systemPrompt: "BASE" },
      ctx,
    );
    assert.ok(result.systemPrompt.includes("ADHD MODE ACTIVE"));
    assert.ok(result.systemPrompt.includes("BASE"));
    assert.ok(result.systemPrompt.includes("Lead with the next action"));
  });
});

test("/i-have-adhd off deactivates", async () => {
  await withTempHome(async () => {
    const { commands, events, appendedEntries } = createPiHarness();
    const ctx = createCommandContext();

    await commands.get("i-have-adhd").handler("", ctx); // on
    await commands.get("i-have-adhd").handler("off", ctx); // off

    assert.deepEqual(appendedEntries.at(-1), {
      customType: "adhd-mode",
      data: { active: false },
    });

    const result = await events.get("before_agent_start")(
      { systemPrompt: "BASE" },
      ctx,
    );
    assert.equal(result, undefined);
  });
});

test("/i-have-adhd status shows state", async () => {
  await withTempHome(async () => {
    const { commands } = createPiHarness();
    let notified = null;
    const ctx = createCommandContext({
      ui: { notify(msg) { notified = msg; } },
    });

    await commands.get("i-have-adhd").handler("status", ctx);
    assert.ok(notified.includes("OFF"));
  });
});

test("always-on flag file activates on session start", async () => {
  await withTempHome(async (tempHome) => {
    // Create the flag file
    mkdirSync(join(tempHome, ".pi"), { recursive: true });
    writeFileSync(join(tempHome, ".pi", ".i-have-adhd-always"), "");

    const { events } = createPiHarness();
    const ctx = createCommandContext();

    await events.get("session_start")({}, ctx);

    const result = await events.get("before_agent_start")(
      { systemPrompt: "BASE" },
      ctx,
    );
    assert.ok(result.systemPrompt.includes("ADHD MODE ACTIVE"));
  });
});

test("always-on env var activates on session start", async () => {
  await withTempHome(async () => {
    process.env.I_HAVE_ADHD_ALWAYS = "1";

    const { events } = createPiHarness();
    const ctx = createCommandContext();

    await events.get("session_start")({}, ctx);

    const result = await events.get("before_agent_start")(
      { systemPrompt: "BASE" },
      ctx,
    );
    assert.ok(result.systemPrompt.includes("ADHD MODE ACTIVE"));
  });
});

test("persisted session state is restored", async () => {
  await withTempHome(async () => {
    const { events } = createPiHarness();
    const ctx = createCommandContext({
      sessionManager: {
        getEntries: () => [
          { type: "custom", customType: "adhd-mode", data: { active: true } },
        ],
      },
    });

    await events.get("session_start")({}, ctx);

    const result = await events.get("before_agent_start")(
      { systemPrompt: "BASE" },
      ctx,
    );
    assert.ok(result.systemPrompt.includes("ADHD MODE ACTIVE"));
  });
});

test("persisted off state is restored even with always-on flag", async () => {
  await withTempHome(async (tempHome) => {
    mkdirSync(join(tempHome, ".pi"), { recursive: true });
    writeFileSync(join(tempHome, ".pi", ".i-have-adhd-always"), "");

    const { events } = createPiHarness();
    const ctx = createCommandContext({
      sessionManager: {
        getEntries: () => [
          { type: "custom", customType: "adhd-mode", data: { active: false } },
        ],
      },
    });

    await events.get("session_start")({}, ctx);

    const result = await events.get("before_agent_start")(
      { systemPrompt: "BASE" },
      ctx,
    );
    assert.equal(result, undefined); // persisted off wins over always-on
  });
});

test('"stop adhd mode" deactivates via input event', async () => {
  await withTempHome(async () => {
    const { commands, events, appendedEntries } = createPiHarness();
    const ctx = createCommandContext();

    await commands.get("i-have-adhd").handler("", ctx); // on
    assert.equal(appendedEntries.at(-1).data.active, true);

    // Simulate user typing "stop adhd mode"
    await events.get("input")({ text: "stop adhd mode" });

    assert.equal(appendedEntries.at(-1).data.active, false);
  });
});

test('"normal mode" deactivates via input event', async () => {
  await withTempHome(async () => {
    const { commands, events } = createPiHarness();
    const ctx = createCommandContext();

    await commands.get("i-have-adhd").handler("", ctx); // on
    await events.get("input")({ text: "normal mode" });

    const result = await events.get("before_agent_start")(
      { systemPrompt: "BASE" },
      ctx,
    );
    assert.equal(result, undefined);
  });
});

test("deactivation command in mid-sentence does NOT deactivate", async () => {
  await withTempHome(async () => {
    const { commands, events } = createPiHarness();
    const ctx = createCommandContext();

    await commands.get("i-have-adhd").handler("", ctx); // on
    await events.get("input")({ text: "add a normal mode toggle to the settings" });

    const result = await events.get("before_agent_start")(
      { systemPrompt: "BASE" },
      ctx,
    );
    assert.ok(result.systemPrompt.includes("ADHD MODE ACTIVE"));
  });
});

test("input event from extension source is ignored", async () => {
  await withTempHome(async () => {
    const { commands, events, appendedEntries } = createPiHarness();
    const ctx = createCommandContext();

    await commands.get("i-have-adhd").handler("", ctx); // on
    const countBefore = appendedEntries.length;

    await events.get("input")({ source: "extension", text: "stop adhd mode" });

    assert.equal(appendedEntries.length, countBefore); // no new entry
  });
});

// -- Pure function tests --

test("isDeactivationCommand matches exact phrases", () => {
  assert.equal(isDeactivationCommand("stop adhd mode"), true);
  assert.equal(isDeactivationCommand("Stop ADHD Mode"), true);
  assert.equal(isDeactivationCommand("normal mode"), true);
  assert.equal(isDeactivationCommand("normal mode."), true);
  assert.equal(isDeactivationCommand("stop adhd mode!"), true);
});

test("isDeactivationCommand rejects mid-sentence usage", () => {
  assert.equal(isDeactivationCommand("add a normal mode toggle"), false);
  assert.equal(isDeactivationCommand("how do I stop adhd mode from running"), false);
  assert.equal(isDeactivationCommand(""), false);
  assert.equal(isDeactivationCommand(null), false);
});

test("stripFrontmatter removes YAML frontmatter", () => {
  const withFm = "---\nname: test\ndescription: hi\n---\n# Body\nText";
  assert.equal(stripFrontmatter(withFm), "# Body\nText");

  const withoutFm = "# Body\nText";
  assert.equal(stripFrontmatter(withoutFm), "# Body\nText");

  assert.equal(stripFrontmatter(""), "");
});
