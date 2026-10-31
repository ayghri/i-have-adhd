# Persistence through a debug spiral

`case.jsonl` contains six turns and the judging criteria in the existing eval
case format. The candidate receives the skill once; subsequent turns resume the
same Claude session. The baseline receives the same tasks without the skill.
The existing prompt helper strips skill metadata before injection.

This evaluates topic-switch persistence, stopping code suggestions after three
reported failures, and the stop acknowledgment. It does not establish internal
mode state, behavior after stopping, plugin loading, or compaction handling.
Existing Pi smoke tests cover native enable/disable state separately.

## Capture

Validate offline:

```sh
python3 scripts/run_scenario_eval.py validate evals/scenarios/persistence-topic-switch-stop
```

After approving provider spending, run each condition with the same explicit
model, budget, and trial number. For example (each invocation allows up to $1):

```sh
python3 scripts/run_scenario_eval.py run \
  --scenario evals/scenarios/persistence-topic-switch-stop \
  --condition baseline --model <model-id> --trial 1 --budget-usd 1 \
  --output /tmp/adhd-baseline.jsonl
python3 scripts/run_scenario_eval.py run \
  --scenario evals/scenarios/persistence-topic-switch-stop \
  --condition candidate --condition-skill skills/i-have-adhd/SKILL.md \
  --model <model-id> --trial 1 --budget-usd 1 \
  --output /tmp/adhd-candidate.jsonl
```

Output paths must be new. Each successful run saves one response row containing
the complete conversation, compatible with `scripts/judge.py`. Failed captures
leave an empty output file; they cannot be mistaken for completed conversations.
Exit status zero means capture completed, not that the skill passed.

## Judge

Combine the baseline and candidate rows into a new JSONL file. Use the existing
[judge and score workflow](../../README.md#judge-and-score), passing
`--cases evals/scenarios/persistence-topic-switch-stop/case.jsonl` to the judge.
It compares the complete conversations blind using the existing rubric and
release gate. Manual grading is also supported there.

Judge spending is separate: approve it explicitly and configure its provider
spending cap before running. For one pair, use `--retries 0` and a Claude runner
command with `--max-budget-usd`, an explicit model, `--safe-mode`, `--tools ""`,
`--strict-mcp-config`, and `--no-session-persistence`. Record CLI/model versions,
trial numbers, rubric, costs, and results. Stub tests do not verify model adherence.

Capture uses an empty temporary working directory, safe mode, no tools, closed
stdin, and a 120-second deadline per call. Budgets must be positive and at most
$25 per capture. Unknown additional spend after timeouts or malformed responses
is reported as unknown. Safe mode retains authentication and managed policies;
Claude sessions may persist in its configured storage. Live calls send the
scenario, candidate skill when selected, and conversation to the provider.
