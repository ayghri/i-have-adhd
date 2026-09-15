// Test driver for the OpenCode plugin. Imports the plugin at argv[2] and runs
// one of its hooks depending on argv[3]:
//
//   (default)  runs `experimental.chat.system.transform` against an empty
//              system prompt and prints the resulting system text so tests
//              can assert on the injected banner. Nothing is printed when the
//              hook injects nothing (always-on flag absent).
//   config     runs the `config` hook twice, seeded by optional JSON at argv[4],
//              and prints the resulting config to check registration, overrides,
//              and idempotency without a running OpenCode server.
import { pathToFileURL } from 'node:url';

const pluginPath = process.argv[2];
const mode = process.argv[3];
const { default: init } = await import(pathToFileURL(pluginPath).href);
const hooks = await init();

if (mode === 'config') {
  const config = JSON.parse(process.argv[4] || "{}");
  await hooks.config(config);
  await hooks.config(config);
  process.stdout.write(JSON.stringify(config));
} else {
  const output = { system: [] };
  await hooks['experimental.chat.system.transform']({}, output);
  process.stdout.write(output.system.join('\n---SEP---\n'));
}
