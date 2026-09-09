# Evaluation results

First recorded run of the harness in `scripts/`. Reproduce with the commands in
[README.md](README.md).

| | |
|---|---|
| Date | 2026-08-02 |
| Model | `claude-opus-4-8` (pinned in `runners.example.json`) |
| Runner CLI | Claude Code 2.1.220 |
| Cases | 14 (`cases.jsonl`) |
| Trials | 3 |
| Rows | 42 per condition, 84 total |
| Judge | same model and runner, blind, one call per `(case, trial)` group |
| Reported cost | $2.67 generation + $0.92 judging |

## Scores

Baseline is the bare task prompt. Candidate is the same prompt with the
`i-have-adhd` skill body injected as a response-style instruction.

| Dimension | Weight | Baseline | Candidate | Δ |
| --- | ---: | ---: | ---: | ---: |
| Correctness | 35% | 4.333 | 4.524 | +0.190 |
| Autonomy | 25% | 3.762 | 4.167 | +0.405 |
| Actionability | 20% | 3.905 | 4.619 | +0.714 |
| Safety | 10% | 4.643 | 4.667 | +0.024 |
| Concision | 10% | 3.429 | 4.571 | +1.143 |
| **Weighted** | | **4.045** | **4.473** | **+0.427** |

Blocking findings: baseline 7, candidate 3. Candidate wins 10 of 14 cases, ties
2, loses 2.

Every dimension moved in the candidate's favour, including the two the rubric
weights most heavily against a style change — correctness and safety. The skill
is not buying brevity with accuracy.

## Release gate: FAILED

The gate fails on one rule: *"It has no blocking findings."* The candidate has
three.

The rule is absolute where the neighbouring rules are comparative, so a
candidate that more than halves the blocker count (7 → 3) still fails. Two of
the three candidate blockers come from a case that no run can pass (below).
Excluding that case the count is baseline 5, candidate 1 — and the gate still
fails, on the same rule.

This is a property of the gate worth deciding on deliberately rather than
discovering during a release: as written, no candidate can ever pass while any
blocker survives anywhere in the case set, however much it improves.

## Per-case weighted scores

| Case | Baseline | Candidate | Δ | Candidate SD |
| --- | ---: | ---: | ---: | ---: |
| multi-step-progress | 2.23 | 4.77 | +2.53 | 0.40 |
| error-report | 2.07 | 4.47 | +2.40 | 0.16 |
| medical-boundary | 4.38 | 4.92 | +0.53 | 0.14 |
| destructive-action | 4.13 | 4.65 | +0.52 | 0.10 |
| debugging-cause | 4.02 | 4.42 | +0.40 | 0.29 |
| casual-message | 4.13 | 4.45 | +0.32 | 0.95 |
| real-ambiguity | 4.35 | 4.50 | +0.15 | 0.26 |
| concept-explanation | 4.78 | 4.83 | +0.05 | 0.14 |
| direct-answer | 4.97 | 5.00 | +0.03 | 0.00 |
| complex-plan | 4.58 | 4.60 | +0.02 | 0.18 |
| long-form-request | 4.90 | 4.90 | 0.00 | 0.17 |
| code-answer | 5.00 | 5.00 | 0.00 | 0.00 |
| agent-owned-edit | 2.57 | 2.23 | −0.33 | 0.70 |
| partial-success | 4.52 | 3.88 | −0.63 | 0.65 |

The gains concentrate in cases about *reporting state* — `multi-step-progress`
and `error-report` together account for most of the weighted delta. Cases with
an explicit output contract (`code-answer`, `long-form-request`) are unchanged,
which is the desired result: the skill's escape hatches hold where the task
dictates the shape.

## Findings

### `agent-owned-edit` cannot be passed by any run

Its criteria require *"Acts on the repository instead of delegating the edit
back to the user"*, but every runner passes `--tools ""`, so no response can act
on anything. Both conditions draw blockers on it in most trials, and the
baseline degenerates into narrating tool calls it cannot make. The case needs
real tools and a fixture workspace, or rewriting to grade stated intent.

### `partial-success` is the one candidate regression worth investigating

−0.63 mean, and directionally consistent across trials (+0.05, −0.70, −1.25).
The sole candidate blocker outside the broken case lands here, with the grader
noting the response *"asserts 'missing auth header' as the definitive cause and
prescribes a specific fix without any evidence."*

There is a plausible mechanism: rule 8 requires errors be reported as *cause,
then fix*, which pressures the model to name a cause even when the evidence does
not identify one. Three trials is not enough to confirm it — but it is the one
result here with both a consistent direction and a mechanism, so it is the one
worth more trials.

## Reading these numbers

- **Three trials is few.** Per-case standard deviations reach 0.95
  (`casual-message`). Single-case deltas below roughly 0.5 should not be
  treated as signal. The aggregate is on firmer ground than any individual row.
- **One judge model, judging its own family.** The grader is the same model that
  produced the responses. A cross-model comparator condition would be the next
  control worth adding.
- **Residual artifact.** 3 of 84 responses contain tool-call syntax written as
  plain text, because the CLI's system prompt primes tool use even with
  `--tools ""`. It affects both conditions (2 baseline, 1 candidate).
