<p align="center">
  <img src="https://em-content.zobj.net/source/apple/391/brain_1f9e0.png" width="120" />
</p>

<h1 align="center">i-have-adhd</h1>

## Install

```bash
git clone https://github.com/ayghri/i-have-adhd ~/i-have-adhd
claude plugin marketplace add ~/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

In Claude Code: `/i-have-adhd`. Stop with `stop adhd mode`. More in [INSTALL.md](./INSTALL.md).

## What it does

A Claude Code skill that stops burying the answer. Action first. Steps numbered. No "Hope this helps!"

No ADHD diagnosis needed!

## What changes

**Before**

> Great question! Let's think about this. Your auth flow has a few moving pieces. We could approach this in a few different ways. Let me know if you want to dig deeper!

**After**

> Run `npm install jsonwebtoken@latest`, then edit `src/auth.ts:42`.
>
> 1. Open `src/auth.ts`
> 2. Replace `verifyToken` (lines 42–58) with the snippet below
> 3. Run `npm test -- auth.spec.ts`
>
> Next: paste the first failing line if any test fails.

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
