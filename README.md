<p align="center">
  <img src="./logo.png" alt="i-have-adhd" width="140" />
</p>
<p align="center">
  <strong align="center">ADHD-friendly outputs. No ADHD diagnosis needed!</strong>
</p>
<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/github/license/ayghri/i-have-adhd?style=flat" alt="License"></a>
</p>


## Install

### Claude Code

```bash
git clone https://github.com/ayghri/i-have-adhd ./i-have-adhd
claude plugin marketplace add ./i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

In Claude Code: `/i-have-adhd`.

To disable: `claude plugin disable i-have-adhd` or use `/plugin disable i-have-adhd` from within CC.

### Codex

```bash
codex plugin marketplace add ayghri/i-have-adhd --ref main
codex plugin add i-have-adhd@i-have-adhd
```

In Codex: use `$i-have-adhd` when you want the output style applied explicitly. The skill can also be invoked implicitly when Codex sees a task that benefits from action-first, ADHD-friendly output.

### Cursor

```bash
npx skills add ayghri/i-have-adhd
```

Global: `npx skills add ayghri/i-have-adhd -g`. Cursor-only: `npx skills add ayghri/i-have-adhd -a cursor -y`.

In Cursor Agent: `/i-have-adhd`. Start a new Agent chat after install.

To uninstall: `npx skills remove i-have-adhd` (or `-g` if installed globally).

<details>
<summary>Manual fallback (clone + copy)</summary>

```bash
mkdir -p ~/.cursor/skills
cp -R /path/to/i-have-adhd/skills/i-have-adhd ~/.cursor/skills/
```

</details>

More in [INSTALL.md](./INSTALL.md).

## What it does

A skill for Claude Code, Codex, and Cursor that stops burying the answer. Action first. Steps numbered. No "Hope this helps!"


## What changes


<table>
<tr>
<td width="50%">

## Before

> Great question! Let me think about this. Your auth flow has a few moving pieces: the middleware, the token verification, and the cookie handling. Looking at `src/auth.ts`, the `verifyToken` function (around lines 42-58) seems to be using an older `jsonwebtoken` API. One approach would be to update the package and rewrite that function. After making the change, you'd want to run the auth tests to confirm nothing breaks. By the way, you might also want to look at your dependency versions overall. Hope this helps! Let me know if you want to dig deeper.

</td>

<td width="50%">

## After

> Run `npm install jsonwebtoken@latest`, then edit `src/auth.ts:42`.
>
> 1. Open `src/auth.ts`
> 2. Replace `verifyToken` (lines 42–58) with the snippet below
> 3. Run `npm test -- auth.spec.ts`
>
> Next: paste the first failing line if any test fails.

</td>
</tr>
</table>


## The rules

10 rules. Full text in [SKILL.md](./skills/i-have-adhd/SKILL.md).

1. Lead with the next action.
2. Number multi-step tasks.
3. End with one concrete next step.
4. Suppress tangents.
5. Restate state every turn.
6. Specific time estimates (minutes, not "a bit").
7. Make wins visible.
8. Matter-of-fact errors.
9. Cap lists at 5 items.
10. No preamble. No recap. No closers.

## Tune it

Edit `skills/i-have-adhd/SKILL.md`. Re-invoke `/i-have-adhd`.

## Credits

Loosely based on *The Adult ADHD Tool Kit* by J. Russell Ramsay and Anthony L. Rostain. Adapted for how an LLM should respond, not how a human should organize their day.

## License

MIT.

Star ⭐ if it saved you one scroll past one "Great question!"
