import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const skillsDir = path.resolve(here, '../../skills');
const skillPath = path.join(skillsDir, 'i-have-adhd', 'SKILL.md');

function ruleset() {
  try {
    return fs.readFileSync(skillPath, 'utf8')
      .replace(/^---[^\S\r\n]*\r?\n[\s\S]*?\r?\n---[^\S\r\n]*(?:\r?\n|$)/, '')
      .replace(/(?:\r?\n)+$/, '');
  } catch {
    return null;
  }
}

function flagPath() {
  const config = process.env.MIMOCODE_HOME
    ? path.join(process.env.MIMOCODE_HOME, 'config')
    : path.join(process.env.XDG_CONFIG_HOME || path.join(os.homedir(), '.config'), 'mimocode');
  return path.join(config, '.i-have-adhd-always');
}

export default {
  id: 'i-have-adhd',
  async server() {
    return {
      config: async (config) => {
        config.skills ||= {};
        config.skills.paths ||= [];
        if (!config.skills.paths.includes(skillsDir)) config.skills.paths.push(skillsDir);
      },
      'experimental.chat.system.transform': async (_input, output) => {
        if (!fs.existsSync(flagPath())) return;
        const content = ruleset();
        if (content === null) return;
        const message = 'ADHD MODE ACTIVE (always-on). The ruleset below applies to every response. '
          + '"stop adhd mode" or "normal mode" requests normal output; delete '
          + 'the MiMo always-on flag to turn it off for good.\n\n' + content;
        if (output.system.length) output.system[output.system.length - 1] += '\n\n' + message;
        else output.system.push(message);
      },
    };
  },
};
