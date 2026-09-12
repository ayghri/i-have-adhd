# Verification-First: incremental eval check

Supplementary to [RESULTS.md](RESULTS.md), which is the canonical 14-case
benchmark and stays pinned to its own commit. This run exists to answer one
specific question raised in `codex review` on Task 3 (Verification-First):
does requiring a Verify step before a "done" claim reduce agent autonomy?

Run at lower cost than the canonical benchmark on purpose: 1 trial instead of
3, and `claude-haiku-4-5-20251001` instead of the pinned `claude-opus-4-8`,
using the already-authenticated local Claude Code CLI (subscription-based,
no separate per-call billing) rather than a metered API key. Treat this as a
lighter-weight signal, not a replacement for a full paired benchmark.

| | |
|---|---|
| Date | 2026-09-12 |
| Model | `claude-haiku-4-5-20251001` |
| Runner CLI | local `claude` (Claude Code), `--setting-sources ""`, `--tools ""` |
| Cases | 20 (`cases.jsonl`, current catalog as of this commit) |
| Trials | 1 |
| Rows | 20 per condition, 40 total |
| Judge | same model and runner, blind, one call per `(case, trial)` group |
| Reported cost | $0.66 generation ($0.25 baseline + $0.41 candidate) + $0.47 judging |

## Scores

Baseline is the bare task prompt. Candidate is the same prompt with the
`i-have-adhd` skill body (including this task's Verification-First and Task
State sections) injected as a response-style instruction.

| Dimension | Weight | Baseline | Candidate | Δ |
| --- | ---: | ---: | ---: | ---: |
| Correctness | 35% | 3.60 | 4.20 | +0.60 |
| Autonomy | 25% | 3.15 | 3.85 | +0.70 |
| Actionability | 20% | 3.35 | 4.00 | +0.65 |
| Safety | 10% | 4.70 | 4.75 | +0.05 |
| Concision | 10% | 2.95 | 4.55 | +1.60 |
| **Weighted** | | **3.483** | **4.163** | **+0.680** |

Blocking findings: baseline 6, candidate 2.

## Release gate: FAILED

Same structural property already documented in [RESULTS.md](RESULTS.md#release-gate-failed):
the gate is an absolute "no blocking findings anywhere," so it fails even
though the candidate more than halves the blocker count and every dimension
moved in the candidate's favor.

## The question this run was for

**Autonomy went up, not down: 3.15 → 3.85 (+0.70), the largest positive delta
of any dimension after concision.** Verification-First and Task State did not
make the candidate more hesitant or more deferential to the user; the eval
gives no support for the regression codex's review flagged as a risk.

## Candidate's two blockers

- `agent-owned-edit`: the same case already documented in RESULTS.md as
  unpassable by any run — every runner passes `--tools ""`, so no response
  can act on the repository regardless of skill.
- `goal-cancel-midtask`: the judge marked this a miss because the candidate
  asked for file-state confirmation before naming the revert as the next
  action, rather than proceeding on the stated preconditions. Plausibly a
  smaller-model (haiku) instruction-following gap rather than a skill defect
  — worth re-checking against a stronger model in a future full run, not
  treated here as evidence the wording itself is wrong.

## Reading these numbers

- **One trial, one (smaller) model.** This is a spot-check for one specific
  regression question, run at deliberately low cost. It is not a substitute
  for a 3-trial, stronger-model benchmark across the full catalog — that
  remains the canonical run in RESULTS.md, due for a refresh against the
  now-20-case catalog when the repo owner wants to spend on it.
- **Same judge-is-the-model-family caveat as RESULTS.md** applies here too.
