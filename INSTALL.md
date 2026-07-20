# Install i-have-adhd

One skill. Installable in Claude Code, Codex, and Cursor.

## TL;DR

### Claude Code

```bash
git clone https://github.com/ayghri/i-have-adhd ./i-have-adhd
claude plugin marketplace add ./i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

Open Claude Code, type `/i-have-adhd`.

To disable: `claude plugin disable i-have-adhd` (or `/plugin disable i-have-adhd` from within Claude Code). Re-enable later with `enable` instead of `disable`.

### Codex

```bash
codex plugin marketplace add ayghri/i-have-adhd --ref main
codex plugin add i-have-adhd@i-have-adhd
```

In Codex, type `$i-have-adhd` to request the output style explicitly.

### Cursor

Project (this workspace):

```bash
npx skills add ayghri/i-have-adhd
```

Global (all Cursor projects):

```bash
npx skills add ayghri/i-have-adhd -g
```

Cursor-only (skip other agents):

```bash
npx skills add ayghri/i-have-adhd -a cursor -y
```

Open a new Cursor Agent chat, type `/i-have-adhd`.

<details>
<summary>Manual fallback (clone + copy)</summary>

```bash
mkdir -p ~/.cursor/skills
cp -R /path/to/i-have-adhd/skills/i-have-adhd ~/.cursor/skills/
```

Replace `/path/to/i-have-adhd` with an existing checkout, such as the checkout used for Claude Code.

Project-only without the CLI:

```bash
mkdir -p .cursor/skills
cp -R /path/to/i-have-adhd/skills/i-have-adhd .cursor/skills/
```

</details>

## Verify

### Claude Code

```bash
claude plugin list
```

Look for `i-have-adhd  (enabled)`.

### Codex

```bash
codex plugin list
```

Look for `i-have-adhd` in the configured `i-have-adhd` marketplace.

### Cursor

```bash
npx skills list
# or, if installed globally:
npx skills ls -g
```

Look for `i-have-adhd`. Or confirm the file exists: `ls ~/.cursor/skills/i-have-adhd/SKILL.md` (global) / `.cursor/skills/i-have-adhd/SKILL.md` (project).

In a new Agent chat, type `/` and look for `i-have-adhd`.

## Update

### Claude Code

```bash
cd ./i-have-adhd && git pull
```

The marketplace re-reads the local checkout. Next Claude Code session picks up changes.

### Codex

```bash
codex plugin marketplace upgrade i-have-adhd
codex plugin remove i-have-adhd
codex plugin add i-have-adhd@i-have-adhd
```

### Cursor

```bash
npx skills update i-have-adhd
# or, if installed globally:
npx skills update -g
```

Start a new Agent chat so Cursor re-reads the skill.

## Uninstall

### Claude Code

```bash
claude plugin uninstall i-have-adhd
claude plugin marketplace remove i-have-adhd
```

### Codex

```bash
codex plugin remove i-have-adhd
codex plugin marketplace remove i-have-adhd
```

### Cursor

```bash
npx skills remove i-have-adhd
# or, if installed globally:
npx skills remove i-have-adhd -g
```

Manual fallback: `rm -rf ~/.cursor/skills/i-have-adhd` or `.cursor/skills/i-have-adhd`.

## Always-on (optional)

### Claude Code

To skip `/i-have-adhd` and apply the rules from message one, add to `~/.claude/CLAUDE.md`:

```markdown
## Output style

Always follow the rules in the `i-have-adhd` skill: action-first, numbered steps, no preamble, no closers, state restated each turn.
```

### Cursor

Add the same text to **Cursor Settings → Rules → User Rules** (applies across projects), or put it in a project rule under `.cursor/rules/` with `alwaysApply: true`.

## Troubleshooting

**`/i-have-adhd` not in autocomplete.** Restart Claude Code. The plugin index is read at startup.

**`claude plugin marketplace add` fails.** Point at the repo root, not at `.claude-plugin/`. The path must contain `.claude-plugin/marketplace.json`.

**Skill activates but model still preambles.** Open a new session. Old context may carry. If it still drifts, tighten the rule wording in `skills/i-have-adhd/SKILL.md`, then re-invoke.

**Want different rules.** Edit `skills/i-have-adhd/SKILL.md`. Re-invoke `/i-have-adhd` (or restart) and the new rules apply.

**Cursor: `/i-have-adhd` missing after install.** Start a new Agent chat. Skills are indexed at session start. Confirm `~/.cursor/skills/i-have-adhd/SKILL.md` exists and that the frontmatter `name` matches the folder name.

**Cursor: skill present but replies still preamble.** Invoke `/i-have-adhd` once in the chat, or use the Always-on User Rule above. Skill auto-invocation is relevance-based; always-on User Rules are stricter.
