// i-have-adhd — OpenCode plugin (universal: sst/opencode 1.17/1.18 + anomalyco/opencode2 beta-18600)
import fs from 'fs'
import os from 'os'
import path from 'path'
import { fileURLToPath } from 'url'
import { define as defineV2 } from '@opencode-ai/plugin/v2/promise'
import * as top from '@opencode-ai/plugin'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const skillPath = path.resolve(__dirname, '../../skills/i-have-adhd/SKILL.md')
const skillsDir = path.resolve(__dirname, '../../skills')
const flagPath = path.join(
  process.env.XDG_CONFIG_HOME || path.join(os.homedir(), '.config'),
  'opencode',
  '.i-have-adhd-always',
)

function rulesetBody() {
  return fs.readFileSync(skillPath, 'utf8')
    .replace(/^---[^\S\r\n]*\r?\n[\s\S]*?\r?\n---[^\S\r\n]*(?:\r?\n|$)/, '')
    .replace(/(?:\r?\n)+$/, '')
}

const activeSessions = new Set()
const define = defineV2 || top.Plugin?.define || top.define || top.default?.define

const plugin = define ? define({
  id: 'i-have-adhd',
  async setup(ctx) {
    if (ctx.skill?.transform) {
      await ctx.skill.transform((draft) => {
        try {
          const body = rulesetBody()
          try { draft.remove('i-have-adhd') } catch {}
          draft.add({
            id: 'i-have-adhd',
            name: 'i-have-adhd',
            description: 'Shape output for a reader with ADHD: lead with the next action, number multi-step work, restate state across turns, suppress tangents, give specific time estimates, make wins visible. Invoke with /i-have-adhd; stays on until "stop adhd mode".',
            location: skillPath,
            content: body,
          })
        } catch {}
      })
    }
    if (ctx.command?.transform) {
      await ctx.command.transform((draft) => {
        draft.add({
          name: 'i-have-adhd',
          description: 'Activate ADHD output shaping for this session',
          async execute({ sessionID }) { activeSessions.add(sessionID) },
        })
      })
    }
    if (ctx.session?.hook) {
      await ctx.session.hook('prompt', (event) => {
        const t = event.prompt?.text || ''
        if (/stop adhd mode|normal mode/i.test(t)) activeSessions.delete(event.sessionID)
      })
      await ctx.session.hook('context', (event) => {
        let on = activeSessions.has(event.sessionID)
        if (!on) try { on = fs.existsSync(flagPath) } catch {}
        if (!on) return
        let body
        try { body = rulesetBody() } catch { return }
        const isAlwaysOn = !activeSessions.has(event.sessionID) && (()=>{try{return fs.existsSync(flagPath)}catch{return false}})()
        const header = isAlwaysOn
          ? `ADHD MODE ACTIVE (always-on). The ruleset below applies to every response. "stop adhd mode" or "normal mode" turns it off for this session; delete ${flagPath} to turn always-on off for good.`
          : 'ADHD MODE ACTIVE (session). The ruleset below applies to every response for the rest of this session.'
        event.system.push({ text: header + '\n\n' + body })
      })
    }
  },
}) : null

export default plugin || (async () => {
  return {
    config: async (config) => {
      config.skills = config.skills || {}
      config.skills.paths = config.skills.paths || []
      if (!config.skills.paths.includes(skillsDir)) config.skills.paths.push(skillsDir)
    },
    'experimental.chat.system.transform': async (_input, output) => {
      let on = false
      try { on = fs.existsSync(flagPath) } catch {}
      if (!on) return
      let body
      try { body = rulesetBody() } catch { return }
      const header = 'ADHD MODE ACTIVE (always-on). The ruleset below applies to every response. "stop adhd mode" or "normal mode" turns it off for this session; delete ' + flagPath + ' to turn always-on off for good.'
      const injected = header + '\n\n' + body
      if (output.system.length > 0) output.system[output.system.length - 1] += '\n\n' + injected
      else output.system.push(injected)
    },
  }
})
