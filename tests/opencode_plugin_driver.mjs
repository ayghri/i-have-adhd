// Test driver for the OpenCode plugin. Imports the plugin at argv[2], runs its
// `experimental.chat.system.transform` hook against an empty system prompt, and
// prints the resulting system text so tests can assert on the injected banner.
// Nothing is printed when the hook injects nothing (always-on flag absent).
import { pathToFileURL } from 'node:url';

const pluginPath = process.argv[2];
const { default: init } = await import(pathToFileURL(pluginPath).href);
const hooks = await init();
const output = { system: [] };
await hooks['experimental.chat.system.transform']({}, output);
process.stdout.write(output.system.join('\n---SEP---\n'));
