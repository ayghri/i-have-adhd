#!/usr/bin/env python3
"""Capture a resumed Claude conversation for the existing judge/score workflow."""

import argparse
import json
import math
import pathlib
import subprocess
import sys
import tempfile
import uuid

import run_evals


CALL_TIMEOUT_SECONDS = 120


def load_scenario(directory: pathlib.Path) -> dict:
    cases = run_evals.load_cases(directory / "case.jsonl")
    errors = run_evals.validate_cases(cases)
    if len(cases) != 1 or errors:
        raise ValueError("Expected one valid scenario case: " + "; ".join(errors))
    case = cases[0]
    turns = case.get("turns")
    if not isinstance(turns, list) or len(turns) < 2:
        raise ValueError("Scenario needs at least two turns")
    seen = set()
    for turn in turns:
        if not isinstance(turn, dict) or any(
            not isinstance(turn.get(key), str) or not turn[key].strip()
            for key in ("id", "prompt")
        ):
            raise ValueError("Each turn needs a non-empty id and prompt")
        if turn["id"] in seen:
            raise ValueError(f"Duplicate turn id: {turn['id']}")
        seen.add(turn["id"])
    return case


def call_claude(command: list[str], workdir: str, spent: float) -> tuple[str, float]:
    """Reject unusable responses while retaining all known reported costs."""
    try:
        result = subprocess.run(
            command,
            cwd=workdir,
            stdin=subprocess.DEVNULL,
            text=True,
            capture_output=True,
            check=False,
            timeout=CALL_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(
            f"Claude timed out; call cost unavailable; reported so far: ${spent:.6f}"
        ) from exc
    try:
        payload = json.loads(result.stdout)
        cost = payload.get("total_cost_usd") if isinstance(payload, dict) else None
        if (
            isinstance(cost, bool)
            or not isinstance(cost, (int, float))
            or cost < 0
            or not math.isfinite(cost)
        ):
            raise ValueError("invalid total_cost_usd")
    except (ValueError, OverflowError) as exc:
        detail = result.stderr.strip() or str(exc)
        raise RuntimeError(
            f"Claude returned invalid JSON or cost ({detail}); call cost unavailable; "
            f"reported so far: ${spent:.6f}"
        ) from exc
    response = payload.get("result")
    if (
        result.returncode
        or payload.get("is_error")
        or str(payload.get("subtype", "")).startswith("error")
        or not isinstance(response, str)
        or not response.strip()
    ):
        detail = result.stderr.strip() or response or "missing response"
        raise RuntimeError(
            f"Claude failed: {detail}; cumulative reported cost: ${spent + cost:.6f}"
        )
    return response.strip(), float(cost)


def run_scenario(args: argparse.Namespace) -> int:
    case = load_scenario(args.scenario)
    if not 0 < args.budget_usd <= 25 or args.trial < 1:
        raise ValueError("Budget must be in (0, 25]; trial must be positive")
    first_prompt = run_evals._condition_prompt(
        case["turns"][0]["prompt"], args.condition, args.condition_skill
    )
    if args.condition == "candidate" and not run_evals._strip_frontmatter(
        args.condition_skill.read_text(encoding="utf-8")
    ).strip():
        raise ValueError("Candidate skill cannot be empty")

    session_id = str(uuid.uuid4())
    spent = 0.0
    transcript = []
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with (
        args.output.open("x", encoding="utf-8") as destination,
        tempfile.TemporaryDirectory(prefix="scenario-eval-") as workdir,
    ):
        for index, turn in enumerate(case["turns"]):
            # Round down so the CLI never receives more than the remaining budget.
            remaining = math.floor((args.budget_usd - spent) * 1_000_000) / 1_000_000
            if remaining <= 0:
                raise RuntimeError(f"Budget exhausted; reported cost: ${spent:.6f}")
            command = [
                "claude", "--safe-mode", "--strict-mcp-config", "--print",
                "--output-format", "json", "--model", args.model, "--tools", "",
                "--resume" if index else "--session-id", session_id,
                "--max-budget-usd", f"{remaining:.6f}",
                first_prompt if index == 0 else turn["prompt"],
            ]
            response, cost = call_claude(command, workdir, spent)
            spent += cost
            if spent > args.budget_usd:
                raise RuntimeError(f"Budget exceeded; reported cost: ${spent:.6f}")
            transcript.append({
                "turn_id": turn["id"],
                "prompt": turn["prompt"],
                "response": response,
            })
        row = {
            "case_id": case["id"],
            "trial": args.trial,
            "condition": args.condition,
            "runner": f"claude:{args.model}",
            "session_id": session_id,
            "response": json.dumps(transcript, ensure_ascii=False),
            "cost_usd": spent,
        }
        destination.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Conversation saved to {args.output}; reported cost: ${spent:.6f}. Not graded.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate")
    validate.add_argument("scenario", type=pathlib.Path)
    run = commands.add_parser("run")
    run.add_argument("--scenario", type=pathlib.Path, required=True)
    run.add_argument("--condition", choices=("baseline", "candidate"), required=True)
    run.add_argument("--condition-skill", type=pathlib.Path)
    run.add_argument("--model", required=True)
    run.add_argument("--trial", type=int, default=1)
    run.add_argument("--budget-usd", type=float, required=True)
    run.add_argument("--output", type=pathlib.Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "validate":
            load_scenario(args.scenario)
            print(f"Valid scenario: {args.scenario.name}")
            return 0
        return run_scenario(args)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
