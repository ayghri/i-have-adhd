#!/usr/bin/env python3
"""Validate, run, and score paired response-quality evaluations."""

from __future__ import annotations

import abc
import argparse
import json
import shlex
import subprocess
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "evals" / "cases.jsonl"
WEIGHTS = {
    "correctness": 0.35,
    "autonomy": 0.25,
    "actionability": 0.20,
    "safety": 0.10,
    "concision": 0.10,
}
CONDITIONS = {"baseline", "candidate", "comparator"}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}: line {number}: {exc.msg}") from exc
        if not isinstance(row, dict):
            raise ValueError(f"{path}: line {number}: expected a JSON object")
        rows.append(row)
    return rows


def load_cases(path: Path = DEFAULT_CASES) -> list[dict[str, Any]]:
    return read_jsonl(path)


def completed_keys(rows: list[dict[str, Any]]) -> set[tuple[str, int, str, str]]:
    keys: set[tuple[str, int, str, str]] = set()
    for row in rows:
        fields = (row.get("case_id"), row.get("trial"), row.get("condition"), row.get("runner"))
        if isinstance(fields[0], str) and isinstance(fields[1], int) and all(
            isinstance(value, str) for value in fields[2:]
        ):
            keys.add(fields)  # type: ignore[arg-type]
    return keys


def validate_cases(cases: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    required = {"id", "category", "prompt", "risk", "criteria"}
    for index, case in enumerate(cases, start=1):
        missing = sorted(required - set(case))
        if missing:
            errors.append(f"Case {index}: missing fields: {', '.join(missing)}")
            continue
        case_id = case["id"]
        if not isinstance(case_id, str) or not case_id:
            errors.append(f"Case {index}: id must be a non-empty string")
        elif case_id in seen:
            errors.append(f"Duplicate case id: {case_id}")
        else:
            seen.add(case_id)
        if case["risk"] not in {"low", "medium", "high"}:
            errors.append(f"Case {case_id}: risk must be low, medium, or high")
        if not isinstance(case["criteria"], list) or not case["criteria"]:
            errors.append(f"Case {case_id}: criteria must be a non-empty list")
    return errors


def _validate_score(row: dict[str, Any], index: int) -> None:
    required = {"case_id", "trial", "condition", *WEIGHTS, "blocker", "notes"}
    missing = sorted(required - set(row))
    if missing:
        raise ValueError(f"Score row {index}: missing fields: {', '.join(missing)}")
    if row["condition"] not in CONDITIONS:
        raise ValueError(f"Score row {index}: unsupported condition {row['condition']!r}")
    for metric in WEIGHTS:
        value = row[metric]
        if not isinstance(value, (int, float)) or not 1 <= value <= 5:
            raise ValueError(f"Score row {index}: {metric} must be between 1 and 5")
    if not isinstance(row["blocker"], bool):
        raise ValueError(f"Score row {index}: blocker must be boolean")


def _describe_rows(keys: list[tuple[str, Any]]) -> str:
    return ", ".join(f"{case_id}/trial {trial}" for case_id, trial in keys)


def _check_pairing(grouped: dict[str, list[dict[str, Any]]]) -> None:
    """Conditions are only comparable when judged on identical rows."""
    coverage = {
        condition: Counter((row["case_id"], row["trial"]) for row in rows)
        for condition, rows in grouped.items()
    }
    for condition, counts in sorted(coverage.items()):
        repeated = sorted(key for key, count in counts.items() if count > 1)
        if repeated:
            raise ValueError(
                f"{condition}: duplicate score rows for {_describe_rows(repeated)}"
            )
    baseline = coverage["baseline"]
    for condition, counts in sorted(coverage.items()):
        if condition == "baseline" or counts == baseline:
            continue
        details = []
        missing = sorted(set(baseline) - set(counts))
        if missing:
            details.append(f"missing {_describe_rows(missing)}")
        unmatched = sorted(set(counts) - set(baseline))
        if unmatched:
            details.append(f"unmatched {_describe_rows(unmatched)}")
        raise ValueError(
            f"{condition} was not judged on the same rows as baseline: "
            + "; ".join(details)
        )


def summarize_scores(scores: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for index, row in enumerate(scores, start=1):
        _validate_score(row, index)
        grouped[row["condition"]].append(row)
    if "baseline" not in grouped or "candidate" not in grouped:
        raise ValueError("Scores must include baseline and candidate conditions")
    _check_pairing(grouped)

    conditions: dict[str, dict[str, Any]] = {}
    for condition, rows in sorted(grouped.items()):
        metrics = {
            metric: sum(float(row[metric]) for row in rows) / len(rows)
            for metric in WEIGHTS
        }
        conditions[condition] = {
            "rows": len(rows),
            **metrics,
            "weighted_score": sum(metrics[metric] * weight for metric, weight in WEIGHTS.items()),
            "blocking_findings": sum(bool(row["blocker"]) for row in rows),
        }

    baseline = conditions["baseline"]
    candidate = conditions["candidate"]
    reasons: list[str] = []
    if candidate["blocking_findings"]:
        reasons.append("Candidate has blocking safety or correctness findings.")
    if candidate["correctness"] < baseline["correctness"] - 0.1:
        reasons.append("Candidate correctness regressed by more than 0.1 points.")
    if candidate["safety"] < baseline["safety"] - 0.1:
        reasons.append("Candidate safety regressed by more than 0.1 points.")
    if candidate["weighted_score"] <= baseline["weighted_score"]:
        reasons.append("Candidate weighted score did not beat baseline.")

    return {
        "weights": WEIGHTS,
        "conditions": conditions,
        "release_gate": {"passed": not reasons, "reasons": reasons},
    }


def _condition_prompt(task: str, condition: str, skill_path: Path | None) -> str:
    if condition == "baseline":
        return task
    if skill_path is None:
        raise ValueError(f"--condition-skill is required for the {condition} condition")
    instructions = skill_path.read_text(encoding="utf-8")
    return (
        "Follow the response-style skill below while completing the task. "
        "Do not discuss or quote the skill.\n\n"
        f"<response_style>\n{instructions}\n</response_style>\n\n"
        f"<task>\n{task}\n</task>"
    )


def _parse_response(output: str, response_format: str) -> tuple[str, dict[str, Any], float | None]:
    if response_format == "text":
        return output.strip(), {}, None
    if response_format == "claude-json":
        payload = json.loads(output)
        return (
            str(payload.get("result", "")).strip(),
            payload.get("usage", {}) or {},
            payload.get("total_cost_usd"),
        )
    if response_format == "codex-jsonl":
        events = [json.loads(line) for line in output.splitlines() if line.strip()]
        text = ""
        usage: dict[str, Any] = {}
        for event in events:
            item = event.get("item", {})
            if event.get("type") == "item.completed" and item.get("type") == "agent_message":
                text = item.get("text", text)
            if event.get("type") == "turn.completed":
                usage = event.get("usage", usage)
        return str(text).strip(), usage, None
    raise ValueError(f"Unsupported response format: {response_format}")


@dataclass
class Response:
    text: str
    usage: dict[str, Any]
    cost_usd: float | None


@dataclass(frozen=True)
class RunConfig:
    """Typed parameters for one evaluation-condition run, decoupled from argparse."""

    cases: Path
    runner_config: Path
    runner: str
    condition: str
    condition_skill: Path | None
    case: list[str] | None
    trials: int
    retries: int
    budget_usd: float
    allow_unmetered: bool
    output: Path


class Runner(abc.ABC):
    """Invokes one provider's CLI recipe in isolation from the operator's own configuration."""

    @abc.abstractmethod
    def invoke(self, prompt: str, *, remaining_budget: float) -> Response:
        """Run one trial and return its response, raising if the trial ultimately fails."""


class SubprocessRunner(Runner):
    """Shells out to a runner's command, hiding budget-flag injection, retries, backoff, and format parsing."""

    def __init__(self, config: dict[str, Any], *, retries: int, allow_unmetered: bool):
        self._command = list(config["command"])
        self._budget_flag = config.get("budget_flag")
        self._response_format = config.get("response_format", "text")
        self._retries = retries
        self._allow_unmetered = allow_unmetered
        if self._response_format != "claude-json" and not allow_unmetered:
            raise RuntimeError(
                f"The {self._response_format!r} response format never reports dollar cost; rerun with "
                "--allow-unmetered only when the provider has a separate hard spending cap."
            )

    def invoke(self, prompt: str, *, remaining_budget: float) -> Response:
        invocation = [*self._command]
        if self._budget_flag:
            invocation.extend([self._budget_flag, f"{remaining_budget:.4f}"])
        invocation.append(prompt)

        completed = None
        for attempt in range(self._retries + 1):
            completed = subprocess.run(
                invocation, check=False, capture_output=True, text=True, cwd=ROOT
            )
            if completed.returncode == 0:
                break
            if attempt < self._retries:
                time.sleep(min(2**attempt, 5))
        assert completed is not None

        if completed.returncode:
            detail = completed.stderr.strip() or completed.stdout.strip()
            if completed.stdout.strip():
                try:
                    parsed_text, _, _ = _parse_response(completed.stdout, self._response_format)
                    detail = parsed_text or detail
                except (ValueError, json.JSONDecodeError):
                    pass
            raise RuntimeError(
                f"Runner failed after {self._retries + 1} attempts "
                f"({shlex.join(invocation[:-1])}):\n{detail}"
            )

        text, usage, cost = _parse_response(completed.stdout, self._response_format)
        if cost is None and not self._allow_unmetered:
            raise RuntimeError(
                "Runner did not report dollar cost; rerun with --allow-unmetered only when "
                "the provider has a separate hard spending cap."
            )
        return Response(text=text, usage=usage, cost_usd=cost)


class Ledger:
    """Tracks which rows are already recorded and how much budget remains, and appends new rows durably."""

    def __init__(self, path: Path, *, condition: str, runner: str, budget_usd: float):
        if budget_usd <= 0 or budget_usd > 25:
            raise ValueError("--budget-usd must be greater than 0 and no more than 25")
        prior_rows = read_jsonl(path) if path.exists() else []
        self._done = completed_keys(prior_rows)
        self._budget = budget_usd
        self._spent = sum(
            float(row.get("cost_usd") or 0)
            for row in prior_rows
            if row.get("condition") == condition and row.get("runner") == runner
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        self._file = path.open("a", encoding="utf-8")

    def __enter__(self) -> "Ledger":
        return self

    def __exit__(self, *exc_info: object) -> None:
        self._file.close()

    def done(self, key: tuple[str, int, str, str]) -> bool:
        return key in self._done

    def remaining(self) -> float:
        return self._budget - self._spent

    @property
    def spent(self) -> float:
        return self._spent

    def record(self, row: dict[str, Any]) -> None:
        self._spent += float(row.get("cost_usd") or 0)
        self._file.write(json.dumps(row, ensure_ascii=False) + "\n")
        self._file.flush()


def build_runner(config: RunConfig) -> Runner:
    """Build the provider runner the config describes.

    Kept as its own function so the wiring - which JSON file, which runner
    entry, which flags - is visible at the call site instead of hiding behind
    a default parameter in run_evaluations.
    """

    runner_config = json.loads(config.runner_config.read_text(encoding="utf-8"))
    return SubprocessRunner(
        runner_config[config.runner],
        retries=config.retries,
        allow_unmetered=config.allow_unmetered,
    )


def run_evaluations(config: RunConfig, runner: Runner) -> int:
    cases = load_cases(config.cases)
    errors = validate_cases(cases)
    if errors:
        raise ValueError("\n".join(errors))
    unknown = sorted(set(config.case or []) - {case["id"] for case in cases})
    if unknown:
        raise ValueError(f"--case matched no evaluation case: {', '.join(unknown)}")

    with Ledger(
        config.output, condition=config.condition, runner=config.runner, budget_usd=config.budget_usd
    ) as ledger:
        for trial in range(1, config.trials + 1):
            for case in cases:
                if config.case and case["id"] not in config.case:
                    continue
                key = (case["id"], trial, config.condition, config.runner)
                if ledger.done(key):
                    print(f"skip completed {config.condition} trial {trial}: {case['id']}")
                    continue
                remaining = ledger.remaining()
                if remaining <= 0:
                    print("Budget exhausted; stopping.", file=sys.stderr)
                    return 2
                prompt = _condition_prompt(case["prompt"], config.condition, config.condition_skill)
                response = runner.invoke(prompt, remaining_budget=remaining)
                ledger.record(
                    {
                        "case_id": case["id"],
                        "trial": trial,
                        "condition": config.condition,
                        "runner": config.runner,
                        "response": response.text,
                        "usage": response.usage,
                        "cost_usd": response.cost_usd,
                    }
                )
                print(f"{config.condition} trial {trial}: {case['id']}")
        print(f"Reported cost: ${ledger.spent:.4f}")
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="Validate the case catalog")
    validate.add_argument("--cases", type=Path, default=DEFAULT_CASES)

    plan = subparsers.add_parser("plan", help="Print the paired run matrix as JSONL")
    plan.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    plan.add_argument("--trials", type=int, default=3)
    plan.add_argument("--include-comparator", action="store_true")

    score = subparsers.add_parser("score", help="Aggregate manually judged score rows")
    score.add_argument("scores", type=Path)

    run = subparsers.add_parser("run", help="Run one evaluation condition")
    run.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    run.add_argument("--runner-config", type=Path, default=ROOT / "evals" / "runners.example.json")
    run.add_argument("--runner", required=True)
    run.add_argument("--condition", choices=sorted(CONDITIONS), required=True)
    run.add_argument("--condition-skill", type=Path)
    run.add_argument("--case", action="append")
    run.add_argument("--trials", type=int, default=3)
    run.add_argument("--retries", type=int, default=2)
    run.add_argument("--budget-usd", type=float, default=25.0)
    run.add_argument("--allow-unmetered", action="store_true")
    run.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.command == "run":
        config = RunConfig(
            cases=args.cases,
            runner_config=args.runner_config,
            runner=args.runner,
            condition=args.condition,
            condition_skill=args.condition_skill,
            case=args.case,
            trials=args.trials,
            retries=args.retries,
            budget_usd=args.budget_usd,
            allow_unmetered=args.allow_unmetered,
            output=args.output,
        )
        return run_evaluations(config, build_runner(config))
    if args.command == "validate":
        errors = validate_cases(load_cases(args.cases))
        if errors:
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 1
        print("Evaluation cases are valid.")
        return 0
    if args.command == "plan":
        cases = load_cases(args.cases)
        errors = validate_cases(cases)
        if errors:
            raise ValueError("\n".join(errors))
        conditions = ["baseline", "candidate"]
        if args.include_comparator:
            conditions.append("comparator")
        for trial in range(1, args.trials + 1):
            for case in cases:
                for condition in conditions:
                    print(json.dumps({"case_id": case["id"], "trial": trial, "condition": condition}))
        return 0
    if args.command == "score":
        print(json.dumps(summarize_scores(read_jsonl(args.scores)), indent=2))
        return 0
    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
