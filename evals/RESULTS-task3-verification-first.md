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
| Runner CLI | local `claude` (Claude Code) **v2.1.269**, `--setting-sources ""`, `--tools ""` |
| Cases | 20 (`cases.jsonl` as of commit `b444820`) |
| Candidate skill revision | `skills/i-have-adhd/SKILL.md` at commit `b444820` — predates the later `e9a6643` wording change that broadened Verify to accept non-command checks; not re-run for that change since it only widens what counts as a valid check, it does not change when one is required |
| Trials | 1 |
| Rows | 20 per condition, 60 total |
| Judge | same model and runner, blind, one call per `(case, trial)` group across all three conditions at once |
| Reported cost | $1.04 generation ($0.25 baseline + $0.41 candidate + $0.37 comparator) + $0.60 judging |

## Three conditions, not two

An earlier version of this file compared only baseline (bare prompt) against
candidate (full current skill). That comparison cannot isolate Task 3's
effect: it also includes every prior rule (Response Mode, Task State), so a
delta there is evidence about the whole skill, not about Verification-First
specifically. Fixed per codex review by adding a third condition:

- **baseline** — bare task prompt, no skill.
- **comparator** — the skill as it stood immediately before Task 3 (Response
  Mode + Task State, no Verification-First) — `git show 2363198:skills/i-have-adhd/SKILL.md`.
- **candidate** — `skills/i-have-adhd/SKILL.md` at commit `b444820`, comparator plus Verification-First.

**candidate vs. comparator is the isolated Task 3 delta.** Baseline is kept
for context against the pre-existing benchmark, not for this question.

## Scores

| Dimension | Weight | Baseline | Comparator | Candidate | Δ (candidate − comparator) |
| --- | ---: | ---: | ---: | ---: | ---: |
| Correctness | 35% | 4.075 | 4.25 | 4.525 | +0.275 |
| Autonomy | 25% | 3.425 | 3.65 | 4.175 | **+0.525** |
| Actionability | 20% | 3.55 | 4.05 | 4.10 | +0.05 |
| Safety | 10% | 4.65 | 4.725 | 4.775 | +0.05 |
| Concision | 10% | 2.85 | 4.575 | 4.45 | −0.125 |
| **Weighted** | | **3.742** | **4.140** | **4.370** | **+0.230** |

Blocking findings: baseline 3, comparator 3, candidate 1.

## Release gate: FAILED

Same structural property already documented in [RESULTS.md](RESULTS.md#release-gate-failed):
the gate is an absolute "no blocking findings anywhere," so it fails even
though candidate has the fewest blockers of the three conditions and the
highest weighted score.

## The question this run was for

**Autonomy rose from comparator to candidate: 3.65 → 4.175 (+0.525), the
largest dimension delta attributable to Task 3 specifically.** Adding
Verification-First did not make the model more hesitant or more deferential
to the user relative to the skill it was added on top of — the eval gives no
support for the regression codex's review flagged as a risk. Concision is the
one dimension that moved slightly against candidate (−0.125), consistent
with Verification-First asking for an explicit verification statement, which
costs a few words.

## Blockers by condition

- **candidate (1):** `multi-step-progress` — didn't restate step/state or
  name a next action, and pushed information-gathering to the user instead
  of searching proactively.
- **comparator (3):** `casual-message` (misread "thanks" as needing
  clarification), `error-report` (asked for diagnostics instead of
  attempting the fix), `multi-step-progress` (concise, but skipped the
  output contract and made an unsupported time estimate).
- **baseline (3):** not itemized here; see raw judge notes for detail.

Note: `agent-owned-edit`, the case RESULTS.md documents as unpassable by any
run (every runner passes `--tools ""`), did not blocker in this run for any
condition — it did in an earlier two-condition version of this check. That
inconsistency is itself the single-trial-noise caveat below, not a change in
the case's nature.

## On the failed release gate

`codex review` flagged shipping this alongside a failed release gate as a
blocker. Not treated as one here, on the same precedent [RESULTS.md](RESULTS.md#release-gate-failed)
itself sets: the gate in `rubric.md` is absolute ("zero blocking findings
anywhere in the case set"), and RESULTS.md documents plainly that under that
rule "no candidate can ever pass ... however much it improves" — the
currently-shipped, canonical skill has never passed this gate either, and was
merged anyway with that limitation stated rather than hidden. This
supplementary run holds itself to the same standard the repository already
applies to the skill as a whole: report the gate result honestly, including
a failure, rather than treat an unreachable absolute bar as a merge blocker.
Actually revising the gate rule in `rubric.md` (e.g., a blocker-count budget
instead of zero-tolerance) is a real option worth deciding on deliberately,
as RESULTS.md itself suggests — but that is a policy change to the eval
harness itself, out of scope for this task.

## Known gap: not re-run for the debug-spiral wording narrowing

Commit `461bcbc` (after this eval ran) narrowed the debug-spiral trigger to
"no progress," and codex review correctly notes this eval's scored candidate
predates it. Not re-run for it: doing so properly would also need a new
progressive-failure case (three failures across different layers) that
doesn't exist in the catalog yet, and the change only makes the spiral
trigger *less* eager to fire — a safety-neutral-or-better direction, not a
new capability this run's autonomy conclusion depends on. Stopping the
live-eval loop here rather than re-running for every subsequent wording
clarification, consistent with how earlier tasks in this plan capped their
own `codex review` iteration once findings became wording-level rather than
substantive. A progressive-failure case and a follow-up run are reasonable
scope for a future task, not this one.

## Reading these numbers

- **One trial, one (smaller) model, single-run judge noise.** This is a
  spot-check for one specific regression question, run at deliberately low
  cost. Scores and even blocker membership shift somewhat between
  independent 1-trial runs of the same conditions (see the `agent-owned-edit`
  note above) — treat the direction and rough size of the candidate vs.
  comparator delta as the signal, not the exact numbers. This is not a
  substitute for a 3-trial, stronger-model benchmark across the full
  catalog — that remains the canonical run in RESULTS.md, due for a refresh
  against the now-20-case catalog when the repo owner wants to spend on it.
- **Same judge-is-the-model-family caveat as RESULTS.md** applies here too.
