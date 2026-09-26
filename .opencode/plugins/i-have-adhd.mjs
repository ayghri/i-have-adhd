// i-have-adhd — OpenCode V2 plugin.
//
// Mirrors the Claude Code / Codex behaviour for OpenCode: the skill in
// `skills/i-have-adhd/SKILL.md` is the single source of truth for the ruleset.
//
//   • On demand   → registers the skill plus a `/i-have-adhd` command so the
//                   ruleset applies for the rest of the session.
//   • Always-on   → when the opt-in flag file exists, the full ruleset is
//                   appended to the system prompt every turn (the OpenCode
//                   equivalent of the SessionStart hook in hooks/always-on.sh).
//
// V2 migration notes:
//   • The default export must be a definition object with an `id` and an
//     `effect`/`setup` function. The V1 shape, a bare
//     `export default async () => ({...})`, is rejected at load time with
//     "Plugin must export a default definition with an id and an effect or
//     setup function".
//   • The V1 `config` mutation hook is gone. Skills and commands register
//     through `ctx.skill.transform` and `ctx.command.transform`.
//   • `experimental.chat.system.transform` is gone. System-prompt edits go
//     through `ctx.session.hook("context", ...)`.
//
// Opt in to always-on:   touch ~/.config/opencode/.i-have-adhd-always
// Opt back out:          rm ~/.config/opencode/.i-have-adhd-always
//
// Install — add to opencode.json(c). V2 requires a directory, and the field
// is plural:
//   { "plugins": ["/absolute/path/to/i-have-adhd"] }

import fs from 'fs';
import os from 'os';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const skillsDir = path.resolve(__dirname, '../../skills');
const skillPath = path.join(skillsDir, 'i-have-adhd', 'SKILL.md');
const commandPath = path.join(__dirname, '..', 'command', 'i-have-adhd.md');

const SKILL_ID = 'i-have-adhd';
const FALLBACK_DESCRIPTION =
  'Shape output for a reader with ADHD: lead with the next action, number ' +
  'multi-step work, restate state across turns, suppress tangents, give ' +
  'specific time estimates, make wins visible.';

const FALLBACK_PROMPT =
  'Use the `i-have-adhd` skill and apply its ruleset to every response for the ' +
  'rest of this session: lead with the next action, number multi-step work, ' +
  'restate state across turns, suppress tangents, give concrete time estimates, ' +
  'and make wins visible. These rules persist until I say "stop adhd mode" or ' +
  '"normal mode".';

// Always-on opt-in flag, mirroring Claude Code's ~/.claude/.i-have-adhd-always
// but under OpenCode's config dir so the two tools stay independent.
const flagPath = path.join(
  process.env.XDG_CONFIG_HOME || path.join(os.homedir(), '.config'),
  'opencode',
  '.i-have-adhd-always',
);

// JSON is valid YAML frontmatter; share native command metadata without a YAML dependency.
async function commandDefinition() {
  const raw = await fs.promises.readFile(commandPath, 'utf8');
  const match = raw.match(/^---[^\S\r\n]*\r?\n([\s\S]*?)\r?\n---[^\S\r\n]*(?:\r?\n|$)([\s\S]*)$/);
  if (!match) throw new Error('Missing command frontmatter');
  return { description: JSON.parse(match[1]).description, template: match[2].trim() };
}

// Read SKILL.md and strip a leading YAML frontmatter block (--- ... ---).
// Regex and trailing-newline trim match hooks/always-on.mjs so always-on
// injections behave identically across harnesses (see tests/test_always_on_hooks.py).
function rulesetBody() {
  return fs
    .readFileSync(skillPath, 'utf8')
    .replace(/^---[^\S\r\n]*\r?\n[\s\S]*?\r?\n---[^\S\r\n]*(?:\r?\n|$)/, '')
    .replace(/(?:\r?\n)+$/, '');
}

export default {
  id: SKILL_ID,

  async setup(ctx) {
    // Make the skill discoverable, so the `skill` tool and the /i-have-adhd
    // command can both load it.
    try {
      const content = rulesetBody();
      await ctx.skill.transform((editor) => {
        if (editor.get(SKILL_ID)) return;
        editor.add({
          id: SKILL_ID,
          name: SKILL_ID,
          description: FALLBACK_DESCRIPTION,
          path: skillPath,
          content,
        });
      });
    } catch (e) {
      // Missing or malformed SKILL.md must not break command registration.
    }

    // Register /i-have-adhd. A global install loads the plugin from a path with
    // no project-scope `.opencode/command/` directory, so the plugin has to
    // supply the command itself (see #140).
    try {
      const command = await commandDefinition();
      await ctx.command.transform((editor) => {
        editor.add({
          name: SKILL_ID,
          description: command.description || FALLBACK_DESCRIPTION,
          execute: async ({ sessionID, prompt, delivery }) => {
            await ctx.session.prompt({
              ...prompt,
              sessionID,
              text: prompt.text ? `${command.template}\n\n${prompt.text}` : command.template,
              delivery,
            });
          },
        });
      });
    } catch (e) {
      // Missing or malformed command files must not break skill discovery.
    }

    // Always-on: append the ruleset to the system prompt every turn while the
    // flag file exists. "stop adhd mode" turns it off for the session (the
    // model honours the skill's own Persistence rules); deleting the flag
    // turns always-on off for good.
    try {
      await ctx.session.hook('context', (event) => {
        let on = false;
        try {
          on = fs.existsSync(flagPath);
        } catch (e) {}
        if (!on) return;

        let body;
        try {
          body = rulesetBody();
        } catch (e) {
          return;
        }

        const header =
          'ADHD MODE ACTIVE (always-on). The ruleset below applies to every ' +
          'response. "stop adhd mode" or "normal mode" turns it off for this ' +
          'session; delete ' + flagPath + ' to turn always-on off for good.';
        event.system.push({ type: 'text', text: header + '\n\n' + body });
      });
    } catch (e) {
      // Always-on injection is optional; never break plugin load.
    }
  },
};
