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

if (mode === 'command-existing') {
  commands.set('i-have-adhd', { name: 'i-have-adhd', description: 'User command', execute: async () => prompts.push({ text: 'USER COMMAND' }) });
}

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
    list: mode === 'command-unavailable' ? undefined : async () => {
      if (mode === 'command-rejected') throw new Error('listing failed');
      if (mode === 'command-malformed') return { data: [{}] };
      return { data: [...commands.values()].map(({ name, description }) => ({ name, description })) };
    },
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

  if (mode === 'command-collision') {
    skills.set('i-have-adhd', { id: 'i-have-adhd', content: 'USER-OWNED SKILL' });
    await commands.get('i-have-adhd').execute({ sessionID: 'ses_test', prompt: { text: 'User request' }, delivery: 'steer' });
    process.stdout.write(JSON.stringify({ skill: skills.get('i-have-adhd'), prompt: prompts.at(-1) }));
  } else if (mode === 'command-existing' || mode === 'command-unavailable' || mode === 'command-rejected' || mode === 'command-malformed') {
    const entry = commands.get('i-have-adhd');
    if (entry) await entry.execute({ sessionID: 'ses_test', prompt: { text: '' }, delivery: 'steer' });
    process.stdout.write(JSON.stringify({ commands: [...commands.keys()], skills: [...skills.keys()], hook: hooks.has('context'), prompts }));
  } else if (mode === 'skill') {
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
