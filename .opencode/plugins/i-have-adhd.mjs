// OpenCode V1 (1.18.29+) uses server(); V2 uses setup().
// Both register the canonical skill, slash command, and opt-in always-on hook.

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  classifySession,
  logDecision,
} from '../../hooks/session-kind.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const skillsDir = path.resolve(__dirname, '../../skills');
const skillPath = path.join(skillsDir, 'i-have-adhd', 'SKILL.md');
const commandPath = path.join(__dirname, '..', 'command', 'i-have-adhd.md');

const SKILL_ID = 'i-have-adhd';
const ASSUMED_HUMAN_TOAST = 'i-have-adhd: assumed human; rules loaded.';
const FALLBACK_DESCRIPTION =
  'Shape output for a reader with ADHD: lead with the next action, number ' +
  'multi-step work, restate state across turns, suppress tangents, give ' +
  'specific time estimates, make wins visible.';

// Command frontmatter is JSON so both loaders can share metadata without a YAML parser.
async function commandDefinition() {
  const raw = await fs.promises.readFile(commandPath, 'utf8');
  const match = raw.match(/^---[^\S\r\n]*\r?\n([\s\S]*?)\r?\n---[^\S\r\n]*(?:\r?\n|$)([\s\S]*)$/);
  if (!match) throw new Error('Missing command frontmatter');
  return { ...JSON.parse(match[1]), template: match[2].trim() };
}

const flagPath = path.join(
  process.env.XDG_CONFIG_HOME || path.join(os.homedir(), '.config'),
  'opencode',
  '.i-have-adhd-always',
);

// Match the shared hooks' frontmatter stripping and newline handling.
function rulesetBody() {
  return fs
    .readFileSync(skillPath, 'utf8')
    .replace(/^---[^\S\r\n]*\r?\n[\s\S]*?\r?\n---[^\S\r\n]*(?:\r?\n|$)/, '')
    .replace(/(?:\r?\n)+$/, '');
}

const sessionCache = new Map();
let missingSessionLogged = false;

function extractSession(res) {
  if (!res || typeof res !== 'object') return null;
  if (res.error !== undefined) return null;

  if (res.data !== undefined) {
    const data = res.data;
    if (data && typeof data === 'object' && typeof data.id === 'string') {
      return data;
    }
    return null;
  }

  if (typeof res.id === 'string') {
    return res;
  }
  return null;
}

async function lookupSessionParent(sessionID, clientOrCtx, runtime) {
  if (!clientOrCtx) {
    return { error: true, parentID: null };
  }
  try {
    let session = null;
    if (runtime === 'v2') {
      if (typeof clientOrCtx?.session?.get !== 'function') {
        return { error: true, parentID: null };
      }
      const res = await clientOrCtx.session.get({ sessionID });
      session = extractSession(res);
    } else {
      const sessionApi = clientOrCtx?.session;
      if (typeof sessionApi?.get !== 'function') {
        return { error: true, parentID: null };
      }
      const tryGet = async (req) => {
        try {
          const res = await sessionApi.get(req);
          return extractSession(res);
        } catch {
          return null;
        }
      };
      session = await tryGet({ path: { id: sessionID } });
      if (!session) {
        session = await tryGet({ sessionID });
      }
      if (!session) {
        session = await tryGet({ id: sessionID });
      }
    }
    if (!session) {
      return { error: true, parentID: null };
    }
    const parentID = session.parentID ?? session.parent_id ?? null;
    return { error: false, parentID };
  } catch {
    return { error: true, parentID: null };
  }
}

// Only runs after the flag opt-in; OpenCode has no human/non-human signal, so a
// top-level session is assumed human and any child session (parentID) is not.
// Decisions, logs, and toasts are cached per session ID.
async function sessionEntry(value, clientOrCtx, runtime) {
  const sessionID =
    typeof value?.sessionID === 'string' && value.sessionID
      ? value.sessionID
      : typeof value?.sessionId === 'string' && value.sessionId
        ? value.sessionId
        : null;

  if (sessionID && sessionCache.has(sessionID)) {
    return sessionCache.get(sessionID);
  }

  const directParentID =
    typeof value?.parentID === 'string' && value.parentID
      ? value.parentID
      : null;

  let decision;
  if (directParentID) {
    decision = classifySession({
      agent: 'opencode',
      ctx: { parentID: directParentID },
    });
  } else if (sessionID) {
    const lookup = await lookupSessionParent(sessionID, clientOrCtx, runtime);
    if (lookup.error) {
      decision = {
        decision: 'unclear',
        reason: 'opencode-lookup-failed',
        signals: { parentId: 'unknown' },
      };
    } else {
      decision = classifySession({
        agent: 'opencode',
        ctx: { parentID: lookup.parentID },
      });
    }
  } else {
    decision = {
      decision: 'unclear',
      reason: 'opencode-session-id-missing',
      signals: { parentId: 'unknown' },
    };
  }

  const entry = { decision, toasted: false };
  if (sessionID) {
    sessionCache.set(sessionID, entry);
    try {
      logDecision({ agent: 'opencode', ...decision, flagPath });
    } catch {
      // Logging failures never block startup or change a decision.
    }
  } else if (!missingSessionLogged) {
    missingSessionLogged = true;
    try {
      logDecision({ agent: 'opencode', ...decision, flagPath });
    } catch {
      // Logging failures never block startup or change a decision.
    }
  }

  return entry;
}

function alwaysOnInjection() {
  try {
    if (!fs.existsSync(flagPath)) return null;
    const header =
      'ADHD MODE ACTIVE (always-on). The ruleset below applies to every ' +
      'response. "stop adhd mode" or "normal mode" turns it off for this ' +
      'session; delete ' + flagPath + ' to turn always-on off for good.';
    return header + '\n\n' + rulesetBody();
  } catch {
    return null;
  }
}

function extractDeletedSessionId(event) {
  if (typeof event?.data?.sessionID === 'string' && event.data.sessionID) {
    return event.data.sessionID;
  }
  if (
    typeof event?.durable?.aggregateID === 'string' &&
    event.durable.aggregateID.startsWith('ses_')
  ) {
    return event.durable.aggregateID;
  }
  if (typeof event?.properties?.info?.id === 'string' && event.properties.info.id) {
    return event.properties.info.id;
  }
  if (typeof event?.properties?.sessionID === 'string' && event.properties.sessionID) {
    return event.properties.sessionID;
  }
  if (typeof event?.properties?.id === 'string' && event.properties.id) {
    return event.properties.id;
  }
  return null;
}

export default {
  id: SKILL_ID,

  async setup(ctx) {
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
    } catch {
      // Keep the command available if skill registration fails.
    }

    try {
      const command = await commandDefinition();
      await ctx.command.transform((editor) => {
        editor.add({
          name: SKILL_ID,
          description: command.description || FALLBACK_DESCRIPTION,
          execute: ({ sessionID, prompt, delivery }) =>
            ctx.session.prompt({
              ...prompt,
              sessionID,
              text: prompt.text ? `${command.template}\n\n${prompt.text}` : command.template,
              delivery,
            }),
        });
      });
    } catch {
      // Keep skill discovery available if command registration fails.
    }

    try {
      if (typeof ctx.event?.subscribe === 'function') {
        (async () => {
          try {
            const stream = ctx.event.subscribe({ types: ['session.deleted'] });
            if (stream && typeof stream[Symbol.asyncIterator] === 'function') {
              for await (const event of stream) {
                if (event?.type === 'session.deleted') {
                  const id = extractDeletedSessionId(event);
                  if (id) sessionCache.delete(id);
                }
              }
            } else if (typeof stream?.subscribe === 'function') {
              stream.subscribe((event) => {
                if (event?.type === 'session.deleted') {
                  const id = extractDeletedSessionId(event);
                  if (id) sessionCache.delete(id);
                }
              });
            }
          } catch {
            // Subscription failure must not block plugin loading.
          }
        })();
      }
    } catch {
      // Event subscription failure must not block plugin loading.
    }

    try {
      await ctx.session.hook('context', async (event) => {
        const injected = alwaysOnInjection();
        if (!injected) return;
        const entry = await sessionEntry(event, ctx, 'v2');
        if (entry.decision.decision !== 'human') return;
        event.system.push({ type: 'text', text: injected });
      });
    } catch {
      // Optional hook failures must not block plugin loading.
    }
  },

  async server(plugin = {}) {
    return {
      event: async ({ event }) => {
        if (event?.type === 'session.deleted') {
          const id = extractDeletedSessionId(event);
          if (id) sessionCache.delete(id);
        }
      },

      config: async (config) => {
        config.skills = config.skills || {};
        config.skills.paths = config.skills.paths || [];
        if (!config.skills.paths.includes(skillsDir)) config.skills.paths.push(skillsDir);

        // Preserve a native or user-defined command with the same name.
        try {
          config.command = config.command || {};
          if (!config.command[SKILL_ID]) {
            config.command[SKILL_ID] = await commandDefinition();
          }
        } catch {
          // Keep skill discovery available if command registration fails.
        }
      },

      'experimental.chat.system.transform': async (input, output) => {
        const injected = alwaysOnInjection();
        if (!injected) return;

        const entry = await sessionEntry(input, plugin?.client, 'v1');
        if (entry.decision.decision !== 'human') return;

        if (output.system.length > 0) {
          output.system[output.system.length - 1] += '\n\n' + injected;
        } else {
          output.system.push(injected);
        }

        if (!entry.toasted) {
          entry.toasted = true;
          try {
            await plugin?.client?.tui?.showToast?.({
              body: { message: ASSUMED_HUMAN_TOAST, variant: 'info' },
            });
          } catch {
            // V2 and older V1 releases have no toast API; injection still stands.
          }
        }
      },
    };
  },
};
