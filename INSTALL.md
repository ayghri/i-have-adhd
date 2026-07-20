# Install i-have-adhd

A Claude Code plugin. One skill inside.

## TL;DR

### Claude Code

```bash
claude plugin marketplace add ayghri/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

No local clone needed — Claude Code fetches the repo and keeps it updated.

Open Claude Code, type `/i-have-adhd`.

To disable: `claude plugin disable i-have-adhd` (or `/plugin disable i-have-adhd` from within Claude Code). Re-enable later with `enable` instead of `disable`.

### Codex

```bash
codex plugin marketplace add ayghri/i-have-adhd --ref main
codex plugin add i-have-adhd@i-have-adhd
```

In Codex, type `$i-have-adhd` to request the output style explicitly.

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

## Update

### Claude Code

```bash
claude plugin marketplace update i-have-adhd
```

Next Claude Code session picks up changes.

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

**`claude plugin marketplace add` fails.** Use the `owner/repo` form: `claude plugin marketplace add ayghri/i-have-adhd`. If you point it at a local path instead, it must be the repo root (the directory containing `.claude-plugin/marketplace.json`), not `.claude-plugin/` itself.

**Skill activates but model still preambles.** Open a new session. Old context may carry. If it still drifts, tighten the rule wording in `skills/i-have-adhd/SKILL.md`, then re-invoke.

**Want different rules.** Fork the repo, edit `skills/i-have-adhd/SKILL.md`, then install your fork: `claude plugin marketplace add <your-username>/i-have-adhd`. (Or clone locally and `claude plugin marketplace add ./i-have-adhd`.) Re-invoke `/i-have-adhd` and the new rules apply.
