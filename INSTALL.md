# Install i-have-adhd

One skill. Claude Code, Codex, Zed, Antigravity, and any harness that reads agent skills.

<details>
<summary><strong>Claude Code</strong></summary>

### Install

```bash
claude plugin marketplace add ayghri/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

Type `/i-have-adhd`.

### Verify

```bash
claude plugin list
```

### Update

```bash
claude plugin marketplace update i-have-adhd
```

### Uninstall

```bash
claude plugin uninstall i-have-adhd
claude plugin marketplace remove i-have-adhd
```

Or keep it installed and turn it off: `claude plugin disable i-have-adhd`.

### Always-on (optional)

A `SessionStart` hook loads the full ruleset at the start of every session, no `/i-have-adhd` needed:

```bash
touch ~/.claude/.i-have-adhd-always
```

Back to on-demand:

```bash
rm ~/.claude/.i-have-adhd-always
```

The hook only fires when the flag file exists, so installing the plugin changes nothing by itself. Honors `$CLAUDE_CONFIG_DIR` if you've moved your config dir. "stop adhd mode" still turns it off for the current session.

</details>

<details>
<summary><strong>Codex</strong></summary>

### Install

```bash
codex plugin marketplace add ayghri/i-have-adhd --ref main
codex plugin add i-have-adhd@i-have-adhd
```

Type `$i-have-adhd`.

### Verify

```bash
codex plugin list
```

### Update

```bash
codex plugin marketplace upgrade i-have-adhd
codex plugin remove i-have-adhd
codex plugin add i-have-adhd@i-have-adhd
```

### Uninstall

```bash
codex plugin remove i-have-adhd
codex plugin marketplace remove i-have-adhd
```

### Always-on (optional)

Add to `~/.codex/AGENTS.md`:

```markdown
## Output style

The reader has ADHD. Shape every response so it can be acted on:

1. Lead with the answer or next action: command, path, or snippet first.
2. Number multi-step work; one bounded action per step.
3. End with one next action doable in under two minutes.
4. Finish the current issue before raising a new one.
5. Restate progress each turn ("step 3 of 5 done").
6. Give time estimates in concrete units, never "a bit".
7. After a change, show what now works.
8. Errors: state location, cause, and fix. No drama.
9. Cap lists at 5 items.
10. No preamble, no recaps, no closers.

Exceptions: explain fully when asked to explain. Confirm before destructive actions. After three failed fixes, stop and name the doubtful assumption. If the request is ambiguous, ask one short question.
```

</details>

<details>
<summary><strong>Zed</strong></summary>

Zed's Agent reads Agent Skills natively — the same `SKILL.md`, no conversion. (Zed's older "Rules" were replaced by Skills + `AGENTS.md` instructions.)

### Install

In the Agent Panel, open the Skills manager and choose **Create skill from URL** (also available from the command palette as `agent: create skill from url`), then paste:

```
https://github.com/ayghri/i-have-adhd/blob/main/skills/i-have-adhd/SKILL.md
```

Save it in **User** scope for every project, or **Project** scope for one. Then type `/i-have-adhd` in the Agent Panel.

Prefer the filesystem? Clone the repo and drop the skill folder into your user skills directory:

```bash
git clone https://github.com/ayghri/i-have-adhd
cp -R i-have-adhd/skills/i-have-adhd ~/.config/zed/skills/
```

### Verify

Open the Skills manager in the Agent Panel — `i-have-adhd` is listed. Or type `/` and confirm it appears.

### Update

Re-import from the same URL (overwrites), or re-copy the folder after `git pull`.

### Uninstall

Remove `i-have-adhd` from the Skills manager, or delete `~/.config/zed/skills/i-have-adhd`.

### Always-on (optional)

Add to your personal `~/.config/zed/AGENTS.md`:

```markdown
## Output style

Always follow the rules in the `i-have-adhd` skill: action-first, numbered steps, no preamble, no closers, state restated each turn.
```

</details>

<details>
<summary><strong>Antigravity (<code>agy</code>)</strong></summary>

### Install

```bash
agy plugin install https://github.com/ayghri/i-have-adhd
```

### Verify

```bash
agy plugin list
```

### Update

```bash
agy plugin uninstall i-have-adhd
agy plugin install https://github.com/ayghri/i-have-adhd
```

### Uninstall

```bash
agy plugin uninstall i-have-adhd
```

Or keep it installed and turn it off: `agy plugin disable i-have-adhd`.

### Always-on (optional)

Add to `~/.gemini/GEMINI.md`:

```markdown
## Output style

The reader has ADHD. Shape every response so it can be acted on:

1. Lead with the answer or next action: command, path, or snippet first.
2. Number multi-step work; one bounded action per step.
3. End with one next action doable in under two minutes.
4. Finish the current issue before raising a new one.
5. Restate progress each turn ("step 3 of 5 done").
6. Give time estimates in concrete units, never "a bit".
7. After a change, show what now works.
8. Errors: state location, cause, and fix. No drama.
9. Cap lists at 5 items.
10. No preamble, no recaps, no closers.

Exceptions: explain fully when asked to explain. Confirm before destructive actions. After three failed fixes, stop and name the doubtful assumption. If the request is ambiguous, ask one short question.
```

</details>

<details>
<summary><strong>Cursor, OpenCode, Amp, Pi, and any other agent-skills harness</strong></summary>

Works with any harness that reads agent skills. Swap `-a <agent>` for yours.

### Install

```bash
npx skills add ayghri/i-have-adhd                  # this workspace
npx skills add ayghri/i-have-adhd -g               # all projects
npx skills add ayghri/i-have-adhd -a cursor -y     # one agent only
npx skills add ayghri/i-have-adhd -a opencode -y
```

New agent chat, type `/i-have-adhd`.

Without the CLI, copy the skill folder into whatever path your agent scans:

```bash
git clone https://github.com/ayghri/i-have-adhd
mkdir -p ~/.cursor/skills     # Cursor. Use .agents/skills for OpenCode, or your agent's own path
cp -R i-have-adhd/skills/i-have-adhd ~/.cursor/skills/
```

### Verify

```bash
npx skills list
npx skills ls -g    # if installed globally
```

### Update

```bash
npx skills update i-have-adhd
npx skills update -g    # if installed globally
```

### Uninstall

```bash
npx skills remove i-have-adhd
npx skills remove i-have-adhd -g    # if installed globally
```

### Always-on (optional)

Paste this into your agent's persistent rules file. Cursor: **Settings → Rules → User Rules**, or a project rule under `.cursor/rules/` with `alwaysApply: true`. OpenCode: `~/.config/opencode/AGENTS.md`.

```markdown
## Output style

The reader has ADHD. Shape every response so it can be acted on:

1. Lead with the answer or next action: command, path, or snippet first.
2. Number multi-step work; one bounded action per step.
3. End with one next action doable in under two minutes.
4. Finish the current issue before raising a new one.
5. Restate progress each turn ("step 3 of 5 done").
6. Give time estimates in concrete units, never "a bit".
7. After a change, show what now works.
8. Errors: state location, cause, and fix. No drama.
9. Cap lists at 5 items.
10. No preamble, no recaps, no closers.

Exceptions: explain fully when asked to explain. Confirm before destructive actions. After three failed fixes, stop and name the doubtful assumption. If the request is ambiguous, ask one short question.
```

</details>

## How activation works

1. **Installed, not invoked.** Nothing happens. `SKILL.md` sets `disable-model-invocation: true`, so the model never sees the skill and never applies the rules on its own.
2. **You type `/i-have-adhd`.** Rules on for that session. "stop adhd mode" or "normal mode" turns them off.
3. **You touch `~/.claude/.i-have-adhd-always`** (Claude Code). A `SessionStart` hook loads the full ruleset from message one, every session.
4. **You add the always-on snippet above** (other harnesses). Keeps the core rules in your agent's persistent context.

No middle ground. If you did not turn it on, it is off.

## Troubleshooting

**`/i-have-adhd` not in autocomplete.** Restart the agent. The plugin index is read at startup.

**Always-on flag has no effect.** Update the plugin (`claude plugin marketplace update i-have-adhd`) and restart. Hooks are read at startup, and the flag needs the plugin version that ships `hooks/hooks.json`.

**`claude plugin marketplace add` fails.** Use the `owner/repo` form. A local path must point at the repo root, not `.claude-plugin/`.

**Installed but replies still preamble.** Open a new session. If it still drifts, tighten the wording in `skills/i-have-adhd/SKILL.md`.

**Want different rules.** Fork, edit `skills/i-have-adhd/SKILL.md`, then swap your copy in:

```bash
claude plugin uninstall i-have-adhd            # drop the upstream copy first:
claude plugin marketplace remove i-have-adhd   # fork and upstream share both names
claude plugin marketplace add <your-username>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

Restart, then re-invoke `/i-have-adhd`.

**Skill missing after `npx skills add`.** Start a new agent chat. Skills are indexed at session start. Confirm the folder landed where your agent scans (`~/.cursor/skills/` for Cursor, `.agents/skills/` for OpenCode) and that the frontmatter `name` matches the folder name.
