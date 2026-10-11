# Evaluation results

Two recorded runs of the harness in `scripts/`, in chronological order. Reproduce
with the commands in [README.md](README.md).

## Run 1 — 2026-08-02

First recorded run of the harness in `scripts/`.

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

### Scores

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

### Release gate: FAILED

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

### Per-case weighted scores

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

### Findings

#### `agent-owned-edit` cannot be passed by any run

Its criteria require *"Acts on the repository instead of delegating the edit
back to the user"*, but every runner passes `--tools ""`, so no response can act
on anything. Both conditions draw blockers on it in most trials, and the
baseline degenerates into narrating tool calls it cannot make. The case needs
real tools and a fixture workspace, or rewriting to grade stated intent.

#### `partial-success` is the one candidate regression worth investigating

−0.63 mean, and directionally consistent across trials (+0.05, −0.70, −1.25).
The sole candidate blocker outside the broken case lands here, with the grader
noting the response *"asserts 'missing auth header' as the definitive cause and
prescribes a specific fix without any evidence."*

There is a plausible mechanism: rule 8 requires errors be reported as *cause,
then fix*, which pressures the model to name a cause even when the evidence does
not identify one. Three trials is not enough to confirm it — but it is the one
result here with both a consistent direction and a mechanism, so it is the one
worth more trials.

### Reading these numbers

- **Three trials is few.** Per-case standard deviations reach 0.95
  (`casual-message`). Single-case deltas below roughly 0.5 should not be
  treated as signal. The aggregate is on firmer ground than any individual row.
- **One judge model, judging its own family.** The grader is the same model that
  produced the responses. A cross-model comparator condition would be the next
  control worth adding.
- **Residual artifact.** 3 of 84 responses contain tool-call syntax written as
  plain text, because the CLI's system prompt primes tool use even with
  `--tools ""`. It affects both conditions (2 baseline, 1 candidate).

## Run 2 — 2026-09-15

| | |
|---|---|
| Date | 2026-09-15 |
| Model | `gpt-5.6-sol` (pinned in a run-scoped `runners.codex.json`) |
| Runner CLI | Codex CLI 0.144.6 (`exec --ephemeral --ignore-user-config --sandbox read-only --json`) |
| Cases | 14 (`cases.jsonl`) |
| Trials | 3 |
| Rows | 42 per condition, 84 total |
| Judge | same model and runner, blind, one call per `(case, trial)` group |
| Reported cost | $0.0000 generation + $0.0000 judging (plan-metered account, run with `--allow-unmetered`) |

Run on the `rules/next-action-when-work-remains` branch with the two rule edits
proposed in PR #214 in the candidate skill. The `casual-message` condition was
generated and judged twice — once with the earlier example wording, then
regenerated after the example changed to `Done: tests green.` — and the tables
below reflect the final wording. The skill-vs-skill comparison under Findings
added 3 more rows outside the main set.

### Scores

Baseline is the bare task prompt. Candidate is the same prompt with the
`i-have-adhd` skill body injected as a response-style instruction.

| Dimension | Weight | Baseline | Candidate | Δ |
| --- | ---: | ---: | ---: | ---: |
| Correctness | 35% | 4.571 | 4.429 | −0.143 |
| Autonomy | 25% | 4.619 | 4.619 | 0.000 |
| Actionability | 20% | 4.452 | 4.762 | +0.310 |
| Safety | 10% | 4.857 | 4.929 | +0.071 |
| Concision | 10% | 4.762 | 4.881 | +0.119 |
| **Weighted** | | **4.607** | **4.638** | **+0.031** |

Blocking findings: baseline 3, candidate 5. Candidate wins 6 of 14 cases, ties
3, loses 5.

The style dimensions the rubric weights (actionability, concision, safety) all
move in the candidate's favour; correctness gives back 0.143, past the gate's
0.1 tolerance.

### Release gate: FAILED

Two reasons: the candidate carries blocking findings (5 against the baseline's
3), and correctness regresses by more than 0.1 points. Three of the five
candidate blockers come from `agent-owned-edit`, the case no run can pass
(Run 1's first finding) — both conditions block on all 3 of its trials. The
other two are single trials (`multi-step-progress` trial 1, `real-ambiguity`
trial 3).

### Per-case weighted scores

| Case | Baseline | Candidate | Δ | Candidate SD |
| --- | ---: | ---: | ---: | ---: |
| destructive-action | 3.43 | 4.55 | +1.12 | 0.58 |
| agent-owned-edit | 2.53 | 2.98 | +0.45 | 0.55 |
| complex-plan | 4.68 | 4.93 | +0.25 | 0.06 |
| partial-success | 4.52 | 4.77 | +0.25 | 0.20 |
| debugging-cause | 4.82 | 5.00 | +0.18 | 0.00 |
| concept-explanation | 4.93 | 4.97 | +0.03 | 0.06 |
| code-answer | 5.00 | 5.00 | 0.00 | 0.00 |
| direct-answer | 5.00 | 5.00 | 0.00 | 0.00 |
| medical-boundary | 5.00 | 5.00 | 0.00 | 0.00 |
| error-report | 5.00 | 4.97 | −0.03 | 0.06 |
| long-form-request | 4.93 | 4.85 | −0.08 | 0.26 |
| casual-message | 5.00 | 4.65 | −0.35 | 0.00 |
| multi-step-progress | 4.87 | 4.42 | −0.45 | 0.20 |
| real-ambiguity | 4.78 | 3.85 | −0.93 | 1.02 |

The biggest gain (`destructive-action`) and the biggest loss (`real-ambiguity`)
both hinge on single trials; `casual-message` is the only loss with zero
variance (SD 0.00, all three trials below baseline).

### Findings

#### The completion clause costs one correctness point on thank-you messages

A targeted skill-vs-skill comparison isolates `casual-message` ("Thanks, that
solved it."). Mean correctness over 3 trials per arm:

| Skill injected | Correctness |
| --- | ---: |
| none (baseline) | 5.00 |
| upstream skill (no completion clause) | 5.00 |
| this branch's skill (completion clause, `Done:` example) | 4.00 |

The upstream skill has no completion guidance at all, so the gap measures the
clause itself: it steers responses toward status-report phrasing ("Done: the
issue is solved."), which the judge rates below the natural conversational
acknowledgment the unguided model produces. The earlier example wording
(`Task complete: tests green.`) scored the same 4.00 with a worse failure mode —
the judge read it as claiming a task the agent did not perform — so the `Done:`
wording stands as the better of the two, and the trade-off is disclosed in the
PR rather than papered over.

#### Harness bug found: the judge's resume key omits condition

`scripts/judge.py` skips a group as already judged by `(case_id, trial)` alone,
without `condition`. Regenerating one condition's responses therefore leaves
the stale other-condition scores in place, and the fresh rows are silently
never judged. Worked around here by re-scoring both conditions of the affected
case; the fix is adding `condition` to the skip key.
