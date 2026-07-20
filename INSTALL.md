# Install i-have-adhd

One portable skill for Qlaw, Claude Code, and Codex.

## TL;DR

### Qlaw

Open [Qlaw](https://qlaw.quick.shopify.io/) and ask:

```text
Install the i-have-adhd skill from https://github.com/ayghri/i-have-adhd
```

Qlaw will fetch `skills/i-have-adhd/SKILL.md` and save it at `/skills/i-have-adhd/SKILL.md`. No plugin wrapper is needed.

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

## Verify

### Qlaw

Open Qlaw's file browser with `/files` and confirm this file exists:

```text
/skills/i-have-adhd/SKILL.md
```

The skill appears in Qlaw's available skills on the next turn.

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

## Always-on (optional)

To skip `/i-have-adhd` and apply the rules from message one, add to `~/.claude/CLAUDE.md`:

```markdown
## Output style

Always follow the rules in the `i-have-adhd` skill: action-first, numbered steps, no preamble, no closers, state restated each turn.
```

## Troubleshooting

**`/i-have-adhd` not in autocomplete.** Restart Claude Code. The plugin index is read at startup.

**`claude plugin marketplace add` fails.** Point at the repo root, not at `.claude-plugin/`. The path must contain `.claude-plugin/marketplace.json`.

**Skill activates but model still preambles.** Open a new session. Old context may carry. If it still drifts, tighten the rule wording in `skills/i-have-adhd/SKILL.md`, then re-invoke.

**Want different rules.** Edit `skills/i-have-adhd/SKILL.md`. Re-invoke `/i-have-adhd` (or restart) and the new rules apply.


## Updating in Qlaw

Ask Qlaw to reinstall the skill from the same GitHub URL. It will fetch the current `skills/i-have-adhd/SKILL.md` and replace the installed copy after confirmation.

## Uninstalling from Qlaw

Delete `/skills/i-have-adhd/` from the Qlaw file browser. Deleting files is irreversible, so Qlaw will ask for confirmation first.
