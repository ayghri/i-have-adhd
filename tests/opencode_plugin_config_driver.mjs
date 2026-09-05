// Test driver for the OpenCode plugin config hook.
// Converts argv[2] with pathToFileURL so Windows absolute paths import.
// Calls `config` and prints the resulting object as JSON.
import { pathToFileURL } from 'node:url';

const pluginPath = process.argv[2];
const href = pluginPath.startsWith('file:')
  ? pluginPath
  : pathToFileURL(pluginPath).href;
const { default: init } = await import(href);
const hooks = await init();
const config = JSON.parse(process.argv[3] || '{}');
await hooks.config(config);
process.stdout.write(JSON.stringify(config));
