// Usage: node driver.mjs <plugin> <skill|command|context|v1-config|v1-context> [config]
// Print registrations as JSON, or the injected system text for context modes.
import { pathToFileURL } from 'node:url';

const pluginPath = process.argv[2];
const mode = process.argv[3];
const { default: definition } = await import(pathToFileURL(pluginPath).href);

const skills = new Map();
const commands = new Map();
const hooks = new Map();
const prompts = [];

const editorFor = (store) => ({
  get: (id) => store.get(id),
  add: (entry) => store.set(entry.id ?? entry.name, entry),
});

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
  },
};

const joined = (event) => event.system.map((part) => part.text ?? String(part)).join('\n---SEP---\n');

if (mode === 'v1-config' || mode === 'v1-context') {
  const v1 = await definition.server();
  if (mode === 'v1-config') {
    const config = JSON.parse(process.argv[4] || '{}');
    await v1.config(config);
    await v1.config(config);
    process.stdout.write(JSON.stringify(config));
  } else {
    const output = { system: [] };
    await v1['experimental.chat.system.transform']({}, output);
    process.stdout.write(output.system.join('\n---SEP---\n'));
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
  } else {
    const handler = hooks.get('context');
    if (!handler) process.exit(0);
    const event = { system: [] };
    await handler(event);
    process.stdout.write(joined(event));
  }
}
