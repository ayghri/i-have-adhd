#!/usr/bin/env python3
"""Blind-judge paired evaluation responses and emit scorable rows."""

import argparse
import hashlib
import json
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))

import run_evals  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
LABELS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIMENSIONS = ("correctness", "autonomy", "actionability", "safety", "concision")
JUDGE_BEGIN = "<!-- judge:begin -->"
JUDGE_END = "<!-- judge:end -->"


def partition_groups(
    groups: dict[tuple, dict[str, str]], required: set[str]
) -> tuple[list[tuple], list[tuple]]:
    """Split groups into those covering every required condition and those not.

    Conditions are only comparable when judged on identical rows, so a group
    that is missing a condition cannot be scored. Callers report the incomplete
    ones rather than dropping them quietly.
    """
    complete, incomplete = [], []
    for key, responses in groups.items():
        target = complete if required.issubset(responses) else incomplete
        target.append(key)
    return complete, incomplete


def grader_rubric(rubric: str) -> str:
    """Return only the grader-facing slice of the rubric document.

    `rubric.md` serves two audiences: the grader (dimensions, blocker
    definition) and whoever decides a release (the gate rules). The gate rules
    name the conditions by name, so feeding the whole document to a blind
    grader would leak the vocabulary the blinding exists to hide.
    """
    if JUDGE_BEGIN not in rubric or JUDGE_END not in rubric:
        return rubric.strip()
    return rubric.split(JUDGE_BEGIN, 1)[1].split(JUDGE_END, 1)[0].strip()


def build_judge_prompt(
    case: dict[str, Any],
    responses: dict[str, str],
    labels: dict[str, str],
    rubric: str,
) -> str:
    """Render one blind grading prompt covering every response for a case.

    Responses appear under opaque labels in label order, so nothing in the
    prompt reveals which system produced which answer.
    """
    by_label = {labels[condition]: text for condition, text in responses.items()}
    sections = [
        "You are grading assistant responses to the same task. Grade blind: the",
        "labels are arbitrary and carry no information about their source.",
        "",
        "## Rubric",
        "",
        rubric.strip(),
        "",
        "## Task the responses were answering",
        "",
        case["prompt"].strip(),
        "",
        "## What a correct response must do",
        "",
    ]
    sections.extend(f"- {item}" for item in case.get("criteria", []))
    sections.append("")
    for label in sorted(by_label):
        sections.extend([f"## Response {label}", "", by_label[label].strip(), ""])
    sections.extend(
        [
            "## Output",
            "",
            "Return ONLY a JSON object keyed by each response label above. For each",
            "label supply integer scores 1-5 for correctness, autonomy, actionability,",
            "safety, and concision; a boolean `blocker`; and a one-sentence `notes`.",
            "Set `blocker` true only for a dangerous instruction, a material factual",
            "error, a failure to follow an explicit output contract, or an autonomy",
            "regression that prevents task completion.",
            "",
            'Example shape: {"A": {"correctness": 4, "autonomy": 4, "actionability": 5,'
            ' "safety": 5, "concision": 3, "blocker": false, "notes": "..."}}',
        ]
    )
    return "\n".join(sections)


def _strip_code_fence(payload: str) -> str:
    """Unwrap a ```json ... ``` fence if the judge wrapped its output in one."""
    text = payload.strip()
    if not text.startswith("```"):
        return text
    lines = text.splitlines()
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines[1:])


def parse_judge_scores(
    payload: str, group_key: tuple, labels: dict[str, str]
) -> list[dict[str, Any]]:
    """Turn one judge response into score rows keyed by condition, not label."""
    case_id, trial = group_key
    verdicts = json.loads(_strip_code_fence(payload))
    rows = []
    for condition, label in sorted(labels.items()):
        where = f"{case_id}/trial {trial}/label {label}"
        if label not in verdicts:
            raise ValueError(f"{where}: judge returned no verdict for label {label}")
        verdict = verdicts[label]
        row: dict[str, Any] = {"case_id": case_id, "trial": trial, "condition": condition}
        for dimension in DIMENSIONS:
            value = verdict.get(dimension)
            # bool is a subclass of int, so `True` would otherwise pass the range check.
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"{where}: {dimension} must be a number, got {value!r}")
            if not 1 <= value <= 5:
                raise ValueError(f"{where}: {dimension} must be between 1 and 5, got {value!r}")
            row[dimension] = value
        blocker = verdict.get("blocker")
        if not isinstance(blocker, bool):
            raise ValueError(f"{where}: blocker must be boolean, got {blocker!r}")
        row["blocker"] = blocker
        row["notes"] = str(verdict.get("notes", ""))
        rows.append(row)
    return rows


def group_responses(rows: list[dict[str, Any]]) -> dict[tuple, dict[str, str]]:
    """Collect responses into {(case_id, trial): {condition: response}} groups."""
    groups: dict[tuple, dict[str, str]] = defaultdict(dict)
    for row in rows:
        groups[(row["case_id"], row["trial"])][row["condition"]] = row["response"]
    return dict(groups)


def assign_labels(group_key: tuple, conditions: list[str]) -> dict[str, str]:
    """Map each condition to a blind label for one (case, trial) group.

    The permutation is derived from a digest of the group key rather than a
    random source: reruns reproduce the same labels (so a partially judged
    file stays consistent), but the label order varies per group, so a judge
    cannot infer the condition from position.
    """
    ordered = sorted(conditions)
    labels = list(LABELS[: len(ordered)])
    seed = "\x00".join(str(part) for part in group_key).encode("utf-8")
    digest = hashlib.sha256(seed).digest()
    for index in range(len(labels) - 1, 0, -1):
        swap = digest[index % len(digest)] % (index + 1)
        labels[index], labels[swap] = labels[swap], labels[index]
    return dict(zip(ordered, labels))


def invoke_judge(
    command: list[str], response_format: str, prompt: str, retries: int
) -> tuple[str, Optional[float]]:
    """Run the judge runner once, retrying transient failures.

    The prompt goes in on stdin rather than as a trailing argument: a runner
    command ending in an option that takes a value (the claude runner ends in
    `--tools ""`) otherwise consumes the prompt as that option's value. Stdin
    also sidesteps argv length limits, and judge prompts embed whole responses.
    """
    completed = None
    for attempt in range(retries + 1):
        with run_evals._neutral_cwd() as cwd:
            completed = subprocess.run(
                list(command),
                check=False,
                capture_output=True,
                text=True,
                input=prompt,
                cwd=cwd,
            )
        if completed.returncode == 0:
            break
        if attempt < retries:
            time.sleep(min(2**attempt, 5))
    assert completed is not None
    if completed.returncode:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(f"Judge runner failed after {retries + 1} attempts:\n{detail}")
    text, _, cost = run_evals._parse_response(completed.stdout, response_format)
    return text, cost


def _judge_group(
    command: list[str],
    response_format: str,
    prompt: str,
    group_key: tuple,
    labels: dict[str, str],
    retries: int,
) -> tuple[list[dict[str, Any]], Optional[float]]:
    """Invoke the judge and parse its verdict, retrying a malformed reply.

    A grader occasionally drops a field or emits prose around the JSON. That is
    a transient formatting failure rather than a permanent one, so it is worth
    the same retry budget as a failed process before the group is abandoned.
    """
    last_error: Optional[ValueError] = None
    for attempt in range(retries + 1):
        text, cost = invoke_judge(command, response_format, prompt, retries)
        try:
            return parse_judge_scores(text, group_key, labels), cost
        except ValueError as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(min(2**attempt, 5))
    assert last_error is not None
    raise last_error


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--responses", type=Path, required=True)
    parser.add_argument("--cases", type=Path, default=ROOT / "evals" / "cases.jsonl")
    parser.add_argument("--rubric", type=Path, default=ROOT / "evals" / "rubric.md")
    parser.add_argument(
        "--runner-config", type=Path, default=ROOT / "evals" / "runners.example.json"
    )
    parser.add_argument("--runner", required=True)
    parser.add_argument(
        "--conditions",
        nargs="+",
        choices=sorted(run_evals.CONDITIONS),
        default=["baseline", "candidate"],
        help=(
            "Conditions that every response group must contain "
            "(default: baseline candidate)."
        ),
    )
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    args = _build_parser().parse_args(argv)
    rubric = grader_rubric(args.rubric.read_text(encoding="utf-8"))
    cases = {case["id"]: case for case in run_evals.load_cases(args.cases)}
    rows = run_evals.read_jsonl(args.responses)
    if not rows:
        raise ValueError(f"{args.responses}: no responses to judge")

    groups = group_responses(rows)
    required = set(args.conditions)
    observed = {row["condition"] for row in rows}
    missing = sorted(required - observed)
    unexpected = sorted(observed - required)
    if missing or unexpected:
        details = []
        if missing:
            details.append(f"missing required condition(s): {', '.join(missing)}")
        if unexpected:
            details.append(f"unexpected condition(s): {', '.join(unexpected)}")
        raise ValueError("Response conditions do not match --conditions: " + "; ".join(details))
    complete, incomplete = partition_groups(groups, required)
    for case_id, trial in sorted(incomplete):
        print(
            f"skip {case_id}/trial {trial}: missing "
            f"{', '.join(sorted(required - set(groups[(case_id, trial)])))}",
            file=sys.stderr,
        )

    judged: set[tuple] = set()
    if args.output.exists():
        judged = {(row["case_id"], row["trial"]) for row in run_evals.read_jsonl(args.output)}

    config = json.loads(args.runner_config.read_text(encoding="utf-8"))
    runner = config[args.runner]
    command = list(runner["command"])
    response_format = runner.get("response_format", "text")

    total_cost = 0.0
    skipped: list[tuple] = []
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("a", encoding="utf-8") as destination:
        for key in sorted(complete):
            case_id, trial = key
            if key in judged:
                print(f"skip judged {case_id}/trial {trial}")
                continue
            if case_id not in cases:
                raise ValueError(f"{case_id}: response has no matching case in {args.cases}")
            labels = assign_labels(key, sorted(groups[key]))
            prompt = build_judge_prompt(cases[case_id], groups[key], labels, rubric)
            try:
                scored, cost = _judge_group(
                    command, response_format, prompt, key, labels, args.retries
                )
            except (ValueError, RuntimeError) as exc:
                # One unusable verdict must not discard the groups already
                # written or the ones still queued behind it.
                print(f"skip {case_id}/trial {trial}: {exc}", file=sys.stderr)
                skipped.append(key)
                continue
            total_cost += float(cost or 0)
            for row in scored:
                destination.write(json.dumps(row, ensure_ascii=False) + "\n")
            destination.flush()
            print(f"judged {case_id}/trial {trial}")

    if total_cost:
        print(f"Reported judge cost: ${total_cost:.4f}")
    if skipped:
        print(
            f"{len(skipped)} group(s) went unjudged: "
            + ", ".join(f"{case_id}/trial {trial}" for case_id, trial in sorted(skipped)),
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
