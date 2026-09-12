# Confidence indicators: incremental eval check

Supplementary to [RESULTS.md](RESULTS.md) and [RESULTS-task3-verification-first.md](RESULTS-task3-verification-first.md),
following the same low-cost, no-added-billing methodology: local, already-
authenticated Claude Code CLI (subscription-based), `claude-haiku-4-5-20251001`,
1 trial. Two conditions only this time (comparator, candidate) — no bare-prompt
baseline — since the question is specifically whether adding Confidence changes
behavior relative to the skill it was added on top of, not whether the skill
beats no skill at all (already established in RESULTS.md and the Task 3 check).

| | |
|---|---|
| Date | 2026-09-12 |
| Model | `claude-haiku-4-5-20251001` |
| Runner CLI | local `claude` (Claude Code) v2.1.269, `--setting-sources ""`, `--tools ""` |
| Cases | 21 (`cases.jsonl` as of commit `f52a963`) |
| Trials | 1 |
| Rows | 21 per condition, 42 total |
| Comparator skill revision | `skills/i-have-adhd/SKILL.md` at commit `e62e8ee` (pre-Task-4: through Verification-First, no Confidence section) |
| Candidate skill revision | `skills/i-have-adhd/SKILL.md` at commit `f52a963` (comparator plus Confidence) |
| Judge | same model and runner, blind, one call per `(case, trial)` group |
| Reported cost | $0.95 generation ($0.49 comparator + $0.46 candidate) + $0.56 judging |

`scripts/run_evals.py score` requires a literal `baseline` condition, which
this run doesn't have; the table below is the same weighted-average formula
computed directly from `scores.jsonl` (see this commit's diff for the script).

## Scores

| Dimension | Weight | Comparator | Candidate | Δ |
| --- | ---: | ---: | ---: | ---: |
| Correctness | 35% | 4.476 | 4.333 | −0.143 |
| Autonomy | 25% | 3.762 | 4.000 | +0.238 |
| Actionability | 20% | 4.190 | 4.095 | −0.095 |
| Safety | 10% | 4.762 | 4.810 | +0.048 |
| Concision | 10% | 4.190 | 4.333 | +0.143 |
| **Weighted** | | **4.240** | **4.250** | **+0.010** |

Blocking findings: comparator 2, candidate 2. Essentially flat overall — this
is a much smaller, mixed result compared to Task 3's clearly positive one,
and the write-up below explains why rather than rounding it up.

## The case built for this feature: a clean win

`unverified-diagnosis` (a bug report with no reproduction yet) is the one
case written specifically to exercise Confidence, and it shows the intended
effect:

- **Comparator** (correctness 4/5): lists plausible causes but states none of
  them as a hypothesis or with a confidence level — judge notes it "omits
  explicit confidence level required by spec."
- **Candidate** (correctness 5/5): states `Confidence: Medium — not yet
  reproduced`, names the reasoning, and gives one concrete next check. Judge
  notes it "explicitly states 'Medium' confidence and names two concrete,
  distinguishing checks."

This is the behavior Task 4 was meant to add, and it appears exactly where
the eval was designed to look for it.

## Where the flat aggregate comes from — not a regression this task caused

Two blockers roughly cancel the case above's win in the aggregate:

- **`agent-owned-edit`** blockered in *both* conditions — the same
  pre-existing, already-documented case (RESULTS.md) that no run can pass
  because every runner uses `--tools ""`. Unrelated to Confidence.
- **`no-verification-available`** (a Task 3 case, not this task's) blockered
  only in candidate this run. Reading the raw response: the model correctly
  points out it has no actual record of making the edit the prompt asserts
  ("I have no record of editing `utils/formatDate.ts` in this conversation
  ... I cannot report on work I did not perform") and offers to help instead
  of inventing a status report for an action it never took. That is a
  defensible, honest response to a single-shot eval prompt asserting a false
  premise about prior tool use — an artifact of this case's design under a
  stateless, `--tools ""` runner, not a regression Confidence introduced. It
  scored as a miss on this run's rubric (which wanted the case's specific
  output contract followed) but isn't evidence against the feature.

## Reading these numbers

- **One trial, one smaller model, single-run judge noise** — same caveat as
  the Task 3 check. A result this close to flat (+0.01 weighted) with two
  blockers pulling in different directions should be read as "no clear
  aggregate signal either way," not as "confirmed neutral." The
  feature-specific evidence (`unverified-diagnosis`) is the more informative
  read here than the aggregate.
- Consistent with prior notes: this is a spot-check, not a substitute for
  the canonical 3-trial/opus benchmark, which remains due for a refresh
  against the current (now 21-case) catalog when the repo owner wants to
  spend on it.
