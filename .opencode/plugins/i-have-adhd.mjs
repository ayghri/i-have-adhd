// i-have-adhd — OpenCode plugin.
//
// Mirrors the Claude Code / Codex behaviour for OpenCode: the skill in
// `skills/i-have-adhd/SKILL.md` is the single source of truth for the ruleset.
//
//   • On demand   — registers the skills directory and a `/i-have-adhd`
//                   command so the ruleset applies for the rest of the session.
//   • Always-on   — when the opt-in flag file exists, the full ruleset is
//                   appended to the system prompt every turn (the OpenCode
//                   equivalent of the SessionStart hook in hooks/always-on.sh).
//
// Opt in to always-on:   touch ~/.config/opencode/.i-have-adhd-always
// Opt back out:          rm ~/.config/opencode/.i-have-adhd-always
//
// Install — add to opencode.json:
//   { "plugin": ["./.opencode/plugins/i-have-adhd.mjs"] }

import fs from 'fs';
import os from 'os';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const skillsDir = path.resolve(__dirname, '../../skills');
const skillPath = path.join(skillsDir, 'i-have-adhd', 'SKILL.md');
const commandPath = path.join(__dirname, '..', 'command', 'i-have-adhd.md');

// Always-on opt-in flag, mirroring Claude Code's ~/.claude/.i-have-adhd-always
// but under OpenCode's config dir so the two tools stay independent.
const flagPath = path.join(
  process.env.XDG_CONFIG_HOME || path.join(os.homedir(), '.config'),
  'opencode',
  '.i-have-adhd-always',
);

// Read SKILL.md and strip a leading YAML frontmatter block (--- ... ---).
// Regex and trailing-newline trim match hooks/always-on.mjs so always-on
// injections behave identically across harnesses (see tests/test_always_on_hooks.py).
function rulesetBody() {
  return fs
    .readFileSync(skillPath, 'utf8')
    .replace(/^---[^\S\r\n]*\r?\n[\s\S]*?\r?\n---[^\S\r\n]*(?:\r?\n|$)/, '')
    .replace(/(?:\r?\n)+$/, '');
}

// OpenCode only auto-discovers `.opencode/command/*.md` in project scope.
// A global plugin install never sees that file, and skills registered via
// `skills.paths` are omitted from the TUI `/` menu (source === "skill").
// Registering through `config.command` makes the loader treat it as
// source "command", which the menu shows. Keep the markdown file as the
// source of truth so checkout-local and plugin-registered copies match.
function slashCommand() {
  const text = fs.readFileSync(commandPath, 'utf8');
  const fence = '---';
  if (!text.startsWith(fence)) {
    return { description: '', template: text.trim() };
  }
  const rest = text.slice(fence.length).replace(/^[\r\n]+/, '');
  const marker = '\n' + fence;
  const idx = rest.indexOf(marker);
  if (idx < 0) {
    return { description: '', template: text.trim() };
  }
  const fm = rest.slice(0, idx);
  const body = rest.slice(idx + marker.length);
  let description = '';
  for (const line of fm.split(/\r?\n/)) {
    if (line.startsWith('description:')) {
      description = line.slice('description:'.length).trim();
      break;
    }
  }
  return { description, template: body.trim() };
}

export default async () => {
  return {
    // Make the skill discoverable (so the `skill` tool and the /i-have-adhd
    // command can load it).
    config: async (config) => {
      config.skills = config.skills || {};
      config.skills.paths = config.skills.paths || [];
      if (!config.skills.paths.includes(skillsDir)) config.skills.paths.push(skillsDir);

      let command;
      try {
        command = slashCommand();
      } catch (e) {
        command = null;
      }
      if (command) {
        config.command = config.command || {};
        config.command['i-have-adhd'] = command;
      }
    },

    // Always-on: append the ruleset to the system prompt every turn while the
    // flag file exists. "stop adhd mode" turns it off for the session (the
    // model honours the skill's own Persistence rules); deleting the flag
    // turns always-on off for good.
    'experimental.chat.system.transform': async (_input, output) => {
      let on = false;
      try { on = fs.existsSync(flagPath); } catch (e) {}
      if (!on) return;

      let body;
      try { body = rulesetBody(); } catch (e) { return; }

      const header =
        'ADHD MODE ACTIVE (always-on). The ruleset below applies to every ' +
        'response. "stop adhd mode" or "normal mode" turns it off for this ' +
        'session; delete ' + flagPath + ' to turn always-on off for good.';
      const injected = header + '\n\n' + body;

      if (output.system.length > 0) {
        output.system[output.system.length - 1] += '\n\n' + injected;
      } else {
        output.system.push(injected);
      }
    },
  };
};
