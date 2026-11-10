// Usage: node driver.mjs <plugin> <skill|command|context|v1-config|v1-context> [options]
// Print registrations as JSON. Context modes print {system, toasts} when either
// is non-empty; `options` is {parentID} for context modes, a config object for
// v1-config.
import { pathToFileURL } from 'node:url';

const pluginPath = process.argv[2];
const mode = process.argv[3];
const options = process.argv[4] ? JSON.parse(process.argv[4]) : undefined;
const { default: definition } = await import(pathToFileURL(pluginPath).href);

const skills = new Map();
const commands = new Map();
const hooks = new Map();
const prompts = [];
const toasts = [];

const editorFor = (store) => ({
  get: (id) => store.get(id),
  add: (entry) => store.set(entry.id ?? entry.name, entry),
});

let lookups = 0;
const sessionStore = new Map();
const eventSubscribers = [];
const eventQueue = [];
const eventWaiters = [];

const pushEvent = (ev) => {
  if (eventWaiters.length > 0) {
    const waiter = eventWaiters.shift();
    waiter(ev);
  } else {
    eventQueue.push(ev);
  }
};

const v2EventStream = {
  [Symbol.asyncIterator]() {
    return {
      async next() {
        if (eventQueue.length > 0) {
          const value = eventQueue.shift();
          return { value, done: false };
        }
        return new Promise((resolve) => {
          eventWaiters.push((value) => resolve({ value, done: false }));
        });
      },
      async return() {
        return { done: true };
      },
    };
  },
};

const seedSession = (s) => {
  if (s && typeof s === 'object' && s.sessionID) {
    if (!sessionStore.has(s.sessionID)) {
      sessionStore.set(s.sessionID, { id: s.sessionID, parentID: s.parentID });
    }
  }
};

const callsList = Array.isArray(options)
  ? options
  : Array.isArray(options?.calls)
    ? options.calls
    : [options || {}];

if (options?.sessions && typeof options.sessions === 'object') {
  for (const [id, s] of Object.entries(options.sessions)) {
    sessionStore.set(id, s);
  }
}
for (const call of callsList) {
  seedSession(call);
}

const handleSessionLookup = async (sessionID) => {
  lookups += 1;
  if (options?.failLookup) {
    throw new Error('Simulated lookup error');
  }
  if (sessionStore.has(sessionID)) {
    const s = sessionStore.get(sessionID);
    if (s === '__ERROR__') {
      throw new Error('Simulated session error');
    }
    return s;
  }
  return { id: sessionID };
};

const v2ctx = {
  skill: {
    transform: async (cb) => {
      cb(editorFor(skills));
      return { dispose: async () => {} };
    },
  },
  command: {
    transform: async (cb) => {
      cb(editorFor(commands));
      return { dispose: async () => {} };
    },
  },
  session: {
    hook: async (name, handler) => {
      hooks.set(name, handler);
      return { dispose: async () => {} };
    },
    prompt: async (input) => {
      prompts.push(input);
    },
    get: options?.noClient ? undefined : async ({ sessionID }) => {
      const res = await handleSessionLookup(sessionID);
      if (res && typeof res === 'object' && 'data' in res && !('id' in res)) {
        return res.data;
      }
      return res;
    },
  },
  event: {
    subscribe: (opts) => {
      if (typeof opts === 'function') {
        return { dispose: () => {} };
      }
      return v2EventStream;
    },
  },
};

// V1 plugins receive the OpenCode client; the toast path is optional.
const v1ctx = {
  client: {
    tui: {
      showToast: async ({ body }) => {
        toasts.push(body?.message);
      },
    },
    session: options?.noClient ? undefined : {
      get: async (req) => {
        const id = req?.path?.id || req?.sessionID || req?.id;
        const res = await handleSessionLookup(id);
        if (res === null || res === undefined) return res;
        if (typeof res === 'object' && ('data' in res || 'error' in res || Object.keys(res).length === 0)) {
          return res;
        }
        return { data: res };
      },
    },
  },
};

const joined = (event) => event.system.map((part) => part.text ?? String(part)).join('\n---SEP---\n');

const emitContext = (system) => {
  if (!system && toasts.length === 0 && lookups === 0) return;
  process.stdout.write(JSON.stringify({ system, toasts, lookups }));
};

if (mode === 'v1-config' || mode === 'v1-context') {
  const v1 = await definition.server(v1ctx);
  if (mode === 'v1-config') {
    const config = options || {};
    await v1.config(config);
    await v1.config(config);
    process.stdout.write(JSON.stringify(config));
  } else if (options?.steps) {
    const systems = [];
    for (const step of options.steps) {
      if (step.type === 'event') {
        if (v1?.event) await v1.event({ event: step.event });
      } else {
        const output = { system: [] };
        await v1['experimental.chat.system.transform'](step.call || {}, output);
        systems.push(output.system.join('\n---SEP---\n'));
      }
    }
    process.stdout.write(JSON.stringify({ systems, system: systems[systems.length - 1], toasts, lookups }));
  } else {
    const calls = Array.isArray(options) ? options : Array.isArray(options?.calls) ? options.calls : [options || {}];
    const systems = [];
    for (const call of calls) {
      const output = { system: [] };
      await v1['experimental.chat.system.transform'](call, output);
      systems.push(output.system.join('\n---SEP---\n'));
    }
    if (Array.isArray(options) || Array.isArray(options?.calls)) {
      process.stdout.write(JSON.stringify({ systems, system: systems[systems.length - 1], toasts, lookups }));
    } else {
      emitContext(systems[0]);
    }
  }
} else {
  await definition.setup(v2ctx);

  if (mode === 'skill') {
    process.stdout.write(JSON.stringify([...skills.values()]));
  } else if (mode === 'command') {
    const out = [...commands.values()].map((command) => ({
      name: command.name,
      description: command.description,
    }));
    const entry = [...commands.values()][0];
    if (entry) {
      await entry.execute({ sessionID: "ses_test", prompt: { text: "" }, delivery: "steer" });
      out[0].template = prompts[prompts.length - 1]?.text;
    }
    process.stdout.write(JSON.stringify(out));
  } else if (options?.steps) {
    const handler = hooks.get('context');
    const systems = [];
    for (const step of options.steps) {
      if (step.type === 'event') {
        pushEvent(step.event);
        await new Promise((resolve) => setImmediate(resolve));
      } else if (handler) {
        const event = { system: [], ...(step.call || {}) };
        await handler(event);
        systems.push(joined(event));
      }
    }
    process.stdout.write(JSON.stringify({ systems, system: systems[systems.length - 1], toasts, lookups }));
  } else {
    const handler = hooks.get('context');
    if (!handler) process.exit(0);
    const calls = Array.isArray(options) ? options : Array.isArray(options?.calls) ? options.calls : [options || {}];
    const systems = [];
    for (const call of calls) {
      const event = { system: [], ...call };
      await handler(event);
      systems.push(joined(event));
    }
    if (Array.isArray(options) || Array.isArray(options?.calls)) {
      process.stdout.write(JSON.stringify({ systems, system: systems[systems.length - 1], toasts, lookups }));
    } else {
      emitContext(systems[0]);
    }
  }
}
