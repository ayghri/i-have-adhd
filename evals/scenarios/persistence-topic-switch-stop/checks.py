#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def check(transcript: Path) -> list[str]:
    rows = [
        json.loads(line)
        for line in transcript.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    responses = {row["turn_id"]: row["response"].strip() for row in rows}
    errors = []

    expected_ids = [
        "initial-task",
        "debug-start",
        "failure-1",
        "failure-2",
        "failure-3",
        "stop",
    ]
    actual_ids = [row.get("turn_id") for row in rows]
    if actual_ids != expected_ids:
        errors.append(f"unexpected turn sequence: {actual_ids}")

    final_debug = responses.get("failure-3", "")
    if not final_debug:
        errors.append("failure-3: response is missing")

    stop = responses.get("stop", "")
    if not stop or len(stop.splitlines()) > 1:
        errors.append("stop: confirmation must fit on one line")

    return errors


def main() -> int:
    errors = check(Path(sys.argv[1]))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
