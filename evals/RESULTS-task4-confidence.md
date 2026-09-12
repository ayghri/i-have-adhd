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

Exact commands, run against a local runner config pointing `command` at the
local `claude` binary with `--model claude-haiku-4-5-20251001` (otherwise
identical to `runners.example.json`'s `claude` entry):

```bash
python3 scripts/run_evals.py run --runner claude --runner-config <local-config> \
  --condition comparator --condition-skill <pre-Task-4 SKILL.md, commit e62e8ee> \
  --trials 1 --budget-usd 3.00 --output evals/results/responses.jsonl

python3 scripts/run_evals.py run --runner claude --runner-config <local-config> \
  --condition candidate --condition-skill skills/i-have-adhd/SKILL.md \
  --trials 1 --budget-usd 3.00 --output evals/results/responses.jsonl

python3 scripts/judge.py --runner claude --runner-config <local-config> \
  --responses evals/results/responses.jsonl \
  --conditions comparator candidate \
  --output evals/results/scores.jsonl
```

`--budget-usd 3.00` was the configured cap per generation run (comparator,
candidate); actual spend was well under it, per the reported costs above.
`judge.py` has no separate budget flag — its cost is reported, not capped.

`scripts/run_evals.py score` requires a literal `baseline` condition, which
this run doesn't have. The table below is the same weighted-average formula
`summarize_scores` uses, computed directly against `scores.jsonl` (gitignored
raw judge output, per `evals/results/`) with:

```python
import json
from collections import defaultdict

WEIGHTS = {"correctness": 0.35, "autonomy": 0.25, "actionability": 0.2, "safety": 0.1, "concision": 0.1}
grouped = defaultdict(list)
for line in open("evals/results/scores.jsonl"):
    row = json.loads(line)
    grouped[row["condition"]].append(row)

for condition, rows in sorted(grouped.items()):
    metrics = {m: sum(float(r[m]) for r in rows) / len(rows) for m in WEIGHTS}
    weighted = sum(metrics[m] * w for m, w in WEIGHTS.items())
    blockers = sum(bool(r["blocker"]) for r in rows)
    print(condition, metrics, weighted, blockers)
```

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

## Release gate: FAILED

Candidate has 2 blocking findings; the gate in `rubric.md` is zero-tolerance.
Not treated as blocking this PR, on the precedent [RESULTS.md](RESULTS.md#release-gate-failed)
and [RESULTS-task3-verification-first.md](RESULTS-task3-verification-first.md#on-the-failed-release-gate)
already set for this exact repository property: the gate has never passed
for the shipped canonical skill either, and the prior supplementary check
merged with the same explicit "FAILED, here's why that isn't blocking" call.
This report follows that established call rather than inventing a stricter
one for this task specifically.

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

## Where the flat aggregate comes from

Breaking down all four blocker rows (two per condition) — one is definitely
unrelated to Confidence, one is structurally unrelated (fails in the
condition that doesn't have the feature), and one is an unresolved possible
regression that this single trial cannot rule out:

- **`agent-owned-edit`** blockered in *both* conditions — the same
  pre-existing, already-documented case (RESULTS.md) that no run can pass
  because every runner uses `--tools ""`. Unrelated to Confidence.
- **`error-report`** blockered only in **comparator**: it asked for files
  instead of stating the failure and giving a fix, deferring work the case's
  prompt already gave it enough information to do. General autonomy
  variance on a single haiku trial, not something Confidence caused (it
  hurts comparator, if anything, in the opposite direction of the flat
  result).
- **`no-verification-available`** (a Task 3 case, not this task's)
  blockered only in **candidate** — and candidate is the one condition that
  differs from comparator by adding Confidence, so a single trial cannot
  rule out Confidence as a contributing cause here the way it can for the
  other two blockers above. Reading the raw response for what's plausible,
  not conclusive: the model points out it has no actual record of making
  the edit the prompt asserts ("I have no record of editing
  `utils/formatDate.ts` in this conversation ... I cannot report on work I
  did not perform") and offers to help instead of inventing a status report
  for an action it never took — a defensible, honest reaction to a
  single-shot eval prompt asserting a false premise about prior tool use,
  and the kind of thing a stateless `--tools ""` runner surfaces regardless
  of skill content. Plausible, not proven: one trial cannot distinguish
  "this case's construction triggered it" from "Confidence made the model
  more willing to refuse an unverifiable premise." Would need more trials
  to tell apart, not asserted as settled here.

Net effect: comparator's extra blocker (`error-report`, definitely unrelated
to Confidence — it's comparator's failure) and candidate's extra blocker
(`no-verification-available`, plausibly but not provenly unrelated) roughly
cancel in the blocker count (2 vs. 2). Between that cancellation and the two
artifacts pulling in different directions, it would be wrong to read the
flat aggregate as proof this feature has no effect — but it would equally be
wrong to claim this run proves it has none of the downside either. The
feature-specific case (`unverified-diagnosis`) remains the more informative
single data point either way.

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
