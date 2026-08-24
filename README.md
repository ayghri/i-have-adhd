<p align="center">
  <img src="./logo.png" alt="i-have-adhd" width="140" />
</p>
<p align="center">
  <strong align="center">ADHD-friendly outputs. No ADHD diagnosis needed!</strong>
</p>
<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/github/license/ayghri/i-have-adhd?style=flat" alt="License"></a>
</p>

<p align="center">
  <strong title="English" aria-label="English">🇬🇧</strong> ·
  <a href=".github/readme/README.zh-CN.md" title="简体中文" aria-label="简体中文">🇨🇳</a> ·
  <a href=".github/readme/README.pt-BR.md" title="Português (Brasil)" aria-label="Português (Brasil)">🇧🇷</a> ·
  <a href=".github/readme/README.ja.md" title="日本語" aria-label="日本語">🇯🇵</a> ·
  <a href=".github/readme/README.vi.md" title="Tiếng Việt" aria-label="Tiếng Việt">🇻🇳</a> ·
  <a href=".github/readme/README.ko.md" title="한국어" aria-label="한국어">🇰🇷</a>
</p>


## Install

Copy/paste into your CLI prompt:

```text
Install the i-have-adhd skill/plugin from https://github.com/ayghri/i-have-adhd, refer to the repo's AGENTS.md for instructions.
```

Or 🔗 [check the installation instructions](INSTALL.md).

## What it does

A skill for your coding assistant that stops it from burying the answer. Action first. Steps numbered. No "Hope this helps!"

## The family (this fork)

This fork expands the single ADHD skill into a **family of output-style skills**, one per cognitive profile. Each skill shapes output to the reader's **profile** — the spiky shape of their abilities across cognitive domains — not a deficit to be fixed. A profile is *spiky*: peaks beside troughs. The rules exist for the troughs; they never fight the peaks.

One condition at a time — plus any number of domain skills **stacked on top** (ADR 0006): rules union, the stricter one wins, each mode turns off by its own stop phrase, and "normal mode" clears the whole stack.

| Skill | Type | Invoke | Stop phrase | Troughs it covers |
|---|---|---|---|---|
| `i-have-adhd` *(upstream, unchanged)* | condition | `/i-have-adhd` | "stop adhd mode" | attention, task initiation, time perception |
| `i-have-dyslexia` | condition | `/i-have-dyslexia` | "stop dyslexia mode" | reading fluency, decoding |
| `i-have-autism` | condition | `/i-have-autism` | "stop autism mode" | literal language, predictability, implicit context |
| `i-have-anxiety` | condition | `/i-have-anxiety` | "stop anxiety mode" | uncertainty tolerance, decision paralysis |
| `i-have-brain-fog` | condition | `/i-have-brain-fog` | "stop brain-fog mode" | working memory, processing speed, fatigue |
| `i-have-dyscalculia` | condition | `/i-have-dyscalculia` | "stop dyscalculia mode" | numeracy — mental arithmetic, quantity comparison |
| `i-have-low-energy` | condition | `/i-have-low-energy` | "stop low-energy mode" | motivation, initiation, energy budgeting |
| `i-have-cognitive-aging` | condition | `/i-have-cognitive-aging` | "stop cognitive-aging mode" | processing speed, place-keeping, familiarity |
| `i-have-low-working-memory` | **domain** | `/i-have-low-working-memory` | "stop low-working-memory mode" | working memory, pure and composable |

Example stack: `/i-have-adhd` + `/i-have-low-working-memory` — ADHD's structure plus working memory's one-instruction-per-message, the stricter rule winning where they meet.

Design docs live in [`docs/`](./docs): the spiky-profile taxonomy ([DOMAINS.md](./docs/DOMAINS.md)), the family's fixed vocabulary ([GLOSSARY.md](./docs/GLOSSARY.md)), the citation list behind every rule ([SOURCES.md](./docs/SOURCES.md)), and the decision records ([docs/adr](./docs/adr)).

`skills/i-have-adhd/SKILL.md` stays byte-identical to upstream. The new skills share its core sections; `scripts/check_shared_core.py` (wired into the test suite) fails the build if they drift.


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

Fork, edit `skills/i-have-adhd/SKILL.md`, then swap your copy in:

```bash
claude plugin uninstall i-have-adhd            # drop the upstream copy first:
claude plugin marketplace remove i-have-adhd   # fork and upstream share both names
claude plugin marketplace add <your-username>/i-have-adhd
claude plugin install i-have-adhd@i-have-adhd
```

Restart Claude Code, then re-invoke `/i-have-adhd`.

## Credits

Loosely based on *The Adult ADHD Tool Kit* by J. Russell Ramsay and Anthony L. Rostain. Adapted for how an LLM should respond, not how a human should organize their day.

## License

MIT.

Star ⭐ if it saved you one scroll past one "Great question!"
