# Evaluations

The harness compares response quality, not just length. Cases live in `cases.jsonl`; the scoring contract lives in `rubric.md`.

## Validate and plan

```bash
python3 scripts/run_evals.py validate
python3 scripts/run_evals.py plan --trials 3 --include-comparator
```

## Run

Run each condition into the same results file. Candidate and comparator instructions are injected from the supplied skill file; task prompts remain identical.

```bash
python3 scripts/run_evals.py run \
  --runner claude \
  --condition baseline \
  --trials 3 \
  --budget-usd 12.50 \
  --output evals/results/responses.jsonl

python3 scripts/run_evals.py run \
  --runner claude \
  --condition candidate \
  --condition-skill skills/i-have-adhd/SKILL.md \
  --trials 3 \
  --budget-usd 12.50 \
  --output evals/results/responses.jsonl
```

The default Claude runner reports dollar cost and receives the remaining condition budget on every call. Runners without cost reporting are rejected unless `--allow-unmetered` is supplied; use that flag only when the provider account has its own hard cap.

Both example runners isolate the call from the operator's own agent configuration: `--setting-sources ""` for Claude, `--ignore-user-config --ephemeral` for Codex. Keep that isolation when adding runners: without it, user-level plugins, hooks, memory, and output styles leak into every condition and shape the responses being judged. The sharpest case is this repo's own always-on flag (`~/.claude/.i-have-adhd-always`), which would inject the full i-have-adhd ruleset into the **baseline** condition and make the comparison measure the skill against itself.

Isolation also drops the operator's saved model and effort settings, so the claude runner pins `--model` explicitly. Keep a pin when editing the runner: without one, the eval silently runs whatever the operator (or the CLI release) defaults to; the model would vary between operators and over time, and per-token cost varies with it. The pinned model is part of the result: record it with published numbers, as below.

Runs are resumable: rerun the same command after a provider failure and completed `(case, trial, condition, runner)` rows are skipped. Each failed call is retried twice by default, while reported spending and reliable cost information permit it; the final provider error is preserved when retries are exhausted.

Generation writes an additional `<output>.attempt-costs.jsonl` file next to the
responses, for example `responses.jsonl.attempt-costs.jsonl`. It records the case,
trial, condition, runner, exit code, and cost of failed or uncertain attempts;
these entries never mark an answer complete. Keep both files together when
resuming or moving a run. The allowance for each retry and later trial subtracts
completed-response costs **and** failed-attempt costs for that condition and
runner. A CLI budget flag receives that remaining amount rounded down to four
decimal places; no call starts if the usable allowance is exhausted. The printed
reported total includes known failed-attempt costs.

A missing, negative, boolean, non-numeric, or non-finite cost is unknown, not free.
In metered mode an uncertain attempt is flushed to the sidecar with
`"cost_usd": null`, then generation stops before retrying. Metered resume also
stops while either file contains unknown/invalid costs for the selected condition
and runner, even when a different case is requested. To recover, reconcile those
entries against the provider's records and replace only their `cost_usd` values
with finite, non-negative dollar amounts; do not delete spending history to
reset the allowance. If reliable costs are unavailable, `--allow-unmetered`
explicitly permits continuing only with a separate provider-side hard cap.
Known costs still reduce its allowance; unknown costs cannot be bounded by this
harness.

Use one generation process per output file. The sidecar is flushed before each
retry, but this is not a transaction log: interruption between a provider call
and writing its result, storage failures, or power loss can leave unrecorded
spending. Reconcile interrupted runs before resuming. Older runs without a
sidecar cannot reconstruct previously discarded failed-call costs. CLI-reported
costs are estimates, not invoices; a provider may exceed its requested call cap.
The harness stops subsequent calls once recorded spending exhausts the budget,
but does not guarantee an invoice ceiling. Successful response rows and the
judge/score input formats are unchanged.

## Measure

Aggregate token usage, reported cost, and response length from the completed responses file:

```bash
python3 scripts/run_evals.py measure evals/results/responses.jsonl
```

The summary reports input/output token totals, reported generation cost, stored
response length, and candidate-minus-baseline deltas. Positive deltas mean more
usage or cost; negative deltas mean less. Read these alongside quality scores.

Comparisons require the same runner and identical `(case_id, trial)` coverage,
without duplicates. If rows include `model`, every row must name the same model.
Older runner output does not record model metadata: `model: null` means model
comparability is unverified. Check the original model/CLI settings yourself;
a matching runner alias alone does not establish the same model or configuration.

Missing costs or token counts produce `null` totals and deltas, not zero. Invalid
negative, boolean, non-finite, or fractional token counts are rejected. A zero
baseline has no meaningful percentage change, so that percentage is `null`.
Claude input totals include cache creation/read tokens; Codex cached input is
already part of its input count and is not added again.

This measures completed generation rows, not total provider billing: judge costs
and failed-attempt costs in the sidecar are excluded. Scenario captures currently omit
token usage, and their response length includes transcript JSON and user prompts.
The command is read-only and makes no model calls.

## Judge and score

`scripts/judge.py` grades the responses and writes the score rows for you:

```bash
python3 scripts/judge.py \
  --runner claude \
  --responses evals/results/responses.jsonl \
  --output evals/results/scores.jsonl
```

It groups responses by `(case_id, trial)` and grades every condition for a case
in one call, so the conditions are compared against each other rather than
scored in isolation. Blinding is structural, not a convention the grader is
asked to respect: each condition is relabelled `A`/`B`/`C` before the prompt is
built, and the label order is permuted per group, so position carries no signal.
The permutation comes from a digest of the group key rather than a random
source, so a resumed run reproduces the labels it used the first time.

Only the region of `rubric.md` between the `<!-- judge:begin -->` and
`<!-- judge:end -->` markers reaches the grader. The release-gate rules below
those markers name the conditions, and sending them to a blind grader would
leak the vocabulary the blinding exists to hide. Keep anything condition-identifying
outside that block.

Runs are resumable the same way generation is: groups already present in the
output file are skipped. A group missing a condition cannot be scored — the
conditions would no longer be judged on identical rows — so it is reported on
stderr and left out rather than silently dropped.

Judging by hand instead is still supported: blind the `condition` field
yourself and write one JSON object per response with these fields.

```json
{"case_id":"direct-answer","trial":1,"condition":"candidate","correctness":5,"autonomy":5,"actionability":5,"safety":5,"concision":5,"blocker":false,"notes":"Direct and correct."}
```

Either way, apply the release gate:

```bash
python3 scripts/run_evals.py score evals/results/scores.jsonl
```

Record the exact CLI and model versions with published results, including measured token and cost numbers. Do not compare conditions produced with different cases, models, trial counts, or rubrics.
