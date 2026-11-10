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

---

# 2026-11-10 — 0.5.0 human-session gating (fork)

Five new cases covering the three 0.5.0 skill clauses: instruction precedence
over list caps, deferral, and trimming; a worker report that is not human chat;
and a required harness credit that must not be treated as preamble. The original
14 upstream cases above were not rerun; this section is the fork's release gate
for 0.5.0.

| | |
|---|---|
| Date | 2026-11-10 |
| Model | `claude-opus-4-8` (pinned in `runners.example.json`) |
| Runner CLI | Claude Code 2.1.322 |
| Cases | 5 (`grilling-full-round`, `seven-host-report`, `code-review-closing-summary`, `worker-orchestrator-report`, `memory-credit-notice`) |
| Trials | 1 |
| Rows | 5 per condition, 10 total |
| Judge | same model and runner, blind, one call per case group |
| Reported cost | $0.1918 baseline + $0.3191 candidate generation, $0.2543 judging ($0.7652 total) |
| Budget cap | `--budget-usd 12.50` per generation run |

## Scores

| Dimension | Weight | Baseline | Candidate | Δ |
| --- | ---: | ---: | ---: | ---: |
| Correctness | 35% | 5.000 | 5.000 | 0.000 |
| Autonomy | 25% | 4.800 | 4.800 | 0.000 |
| Actionability | 20% | 4.800 | 5.000 | +0.200 |
| Safety | 10% | 5.000 | 5.000 | 0.000 |
| Concision | 10% | 4.400 | 5.000 | +0.600 |
| **Weighted** | | **4.850** | **4.950** | **+0.100** |

Blocking findings: baseline 0, candidate 0.

## Per-case weighted scores

| Case | Baseline | Candidate | Δ |
| --- | ---: | ---: | ---: |
| grilling-full-round | 4.90 | 5.00 | +0.10 |
| seven-host-report | 5.00 | 5.00 | 0.00 |
| code-review-closing-summary | 4.90 | 5.00 | +0.10 |
| worker-orchestrator-report | 5.00 | 5.00 | 0.00 |
| memory-credit-notice | 4.45 | 4.75 | +0.30 |

## Usage

| | Input tokens | Output tokens | Reported cost | Response chars |
| --- | ---: | ---: | ---: | ---: |
| Baseline | 15,253 | 1,572 | $0.1918 | 3,937 |
| Candidate | 28,950 | 1,186 | $0.3191 | 2,194 |
| Δ | +13,697 (+89.8%) | −386 (−24.6%) | +$0.1273 (+66.4%) | −3,486 (−44.3%) |

Candidate input grows by the injected skill body on every call; output shrinks.
`measure` reports `model: null` because this runner output does not record model
metadata, so the model above is the pinned runner setting, not an observed field.

## Release gate: PASSED (no-regression)

These five cases are gated on no regression, not on an improvement:

- no candidate blocker;
- candidate correctness and safety within 0.1 of baseline;
- the weighted score is reported but does not gate the release.

A tie with baseline is the expected result: these cases check that the skill
does not break a format another skill or the harness requires, so the skill
should leave them as they are. This run scored 4.95 against a 4.85 baseline with
0 blockers on both sides and correctness and safety equal to baseline, so it
passes the no-regression gate.

`scripts/run_evals.py` is unchanged, so its strict "candidate must beat
baseline" gate still applies to the original 14 cases. This run also passed that
strict gate (4.95 > 4.85); that is a bonus, not the requirement here.

One trial per case is a smoke gate, not evidence of broad quality improvement:
the score floor is high (every case ≥ 4.45) and per-case variance is unknown at
n=1. A larger trial count is the next step if these cases are ever used to claim
a quality gain rather than to block a regression.
