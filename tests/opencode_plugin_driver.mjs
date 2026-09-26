// Test driver for the OpenCode plugin. Imports the plugin at argv[2], calls its
// V2 `setup` with a recording context, and runs one of the registered handlers
// depending on argv[3]:
//
//   (default)  fires the `context` session hook against an empty system prompt
//              and prints the resulting system text so tests can assert on the
//              injected banner. Nothing is printed when the hook injects
//              nothing (always-on flag absent).
//   skill      prints the registered skills as JSON.
//   command    prints the registered commands as JSON, with `template` holding
//              the prompt the command would submit.
//
// V2 note: the plugin default-exports a definition object, so the driver awaits
// `setup(ctx)` instead of calling a bare function.
import { pathToFileURL } from 'node:url';

const pluginPath = process.argv[2];
const mode = process.argv[3];
const { default: definition } = await import(pathToFileURL(pluginPath).href);

const skills = new Map();
const commands = new Map();
const hooks = new Map();
const prompts = [];

const editorFor = (store) => ({
  list: () => [...store.values()],
  get: (id) => store.get(id),
  add: (entry) => store.set(entry.id ?? entry.name, entry),
});

const ctx = {
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

await definition.setup(ctx);

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
  process.stdout.write(event.system.map((part) => part.text ?? String(part)).join('\n---SEP---\n'));
}
