import dataclasses
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import run_evals  # noqa: E402


class EvaluationHarnessTest(unittest.TestCase):
    def test_case_catalog_is_valid_and_balanced(self):
        cases = run_evals.load_cases(ROOT / "evals" / "cases.jsonl")
        errors = run_evals.validate_cases(cases)

        self.assertEqual([], errors)
        self.assertGreaterEqual(len(cases), 12)
        self.assertGreaterEqual(len({case["category"] for case in cases}), 8)

    def test_score_summary_applies_weights_and_release_gates(self):
        scores = []
        for condition, value in (("baseline", 3), ("candidate", 4)):
            scores.append(
                {
                    "case_id": "direct-answer",
                    "trial": 1,
                    "condition": condition,
                    "correctness": value,
                    "autonomy": value,
                    "actionability": value,
                    "safety": value,
                    "concision": value,
                    "blocker": False,
                    "notes": "fixture",
                }
            )

        summary = run_evals.summarize_scores(scores)

        self.assertAlmostEqual(3.0, summary["conditions"]["baseline"]["weighted_score"])
        self.assertAlmostEqual(4.0, summary["conditions"]["candidate"]["weighted_score"])
        self.assertTrue(summary["release_gate"]["passed"])

    def test_candidate_blocker_fails_release_gate(self):
        rows = []
        for condition in ("baseline", "candidate"):
            rows.append(
                {
                    "case_id": "dangerous-action",
                    "trial": 1,
                    "condition": condition,
                    "correctness": 5,
                    "autonomy": 5,
                    "actionability": 5,
                    "safety": 5,
                    "concision": 5,
                    "blocker": condition == "candidate",
                    "notes": "fixture",
                }
            )

        summary = run_evals.summarize_scores(rows)

        self.assertFalse(summary["release_gate"]["passed"])
        self.assertIn("blocking", " ".join(summary["release_gate"]["reasons"]))

    def test_conditions_judged_on_different_cases_are_rejected(self):
        rows = [
            self._score_row("destructive-action", "baseline", 2),
            self._score_row("medical-boundary", "baseline", 2),
            self._score_row("direct-answer", "candidate", 5),
        ]

        with self.assertRaisesRegex(ValueError, "not judged on the same rows"):
            run_evals.summarize_scores(rows)

    def test_duplicate_score_rows_are_rejected(self):
        rows = [
            self._score_row("direct-answer", "baseline", 3),
            self._score_row("direct-answer", "candidate", 4),
            self._score_row("direct-answer", "candidate", 5),
        ]

        with self.assertRaisesRegex(ValueError, "duplicate score rows"):
            run_evals.summarize_scores(rows)

    @staticmethod
    def _score_row(case_id, condition, value, trial=1):
        return {
            "case_id": case_id,
            "trial": trial,
            "condition": condition,
            "correctness": value,
            "autonomy": value,
            "actionability": value,
            "safety": value,
            "concision": value,
            "blocker": False,
            "notes": "fixture",
        }

    def test_duplicate_case_ids_are_rejected(self):
        case = {
            "id": "duplicate",
            "category": "direct-answer",
            "prompt": "What is 2 + 2?",
            "risk": "low",
            "criteria": ["Answers 4."],
        }
        errors = run_evals.validate_cases([case, dict(case)])
        self.assertTrue(any("Duplicate" in error for error in errors))

    def test_jsonl_loader_reports_invalid_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.jsonl"
            path.write_text(json.dumps({"id": "ok"}) + "\nnot-json\n")
            with self.assertRaisesRegex(ValueError, "line 2"):
                run_evals.read_jsonl(path)

    def test_unmetered_runner_is_rejected_before_any_call(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            marker = tmp_path / "ran"
            runner_config = tmp_path / "runners.json"
            runner_config.write_text(
                json.dumps(
                    {
                        "stub": {
                            "command": ["sh", "-c", f"touch {marker} && echo hi"],
                            "response_format": "text",
                        }
                    }
                )
            )
            config = run_evals.RunConfig(
                cases=ROOT / "evals" / "cases.jsonl",
                runner_config=runner_config,
                runner="stub",
                condition="baseline",
                condition_skill=None,
                case=["direct-answer"],
                trials=1,
                retries=0,
                budget_usd=1.0,
                allow_unmetered=False,
                output=tmp_path / "out.jsonl",
            )

            with self.assertRaisesRegex(RuntimeError, "never reports dollar cost"):
                run_evals.build_runner(config)

            self.assertFalse(marker.exists(), "runner was invoked before the rejection")
            self.assertFalse((tmp_path / "out.jsonl").exists())

            config = dataclasses.replace(config, allow_unmetered=True)
            runner = run_evals.build_runner(config)
            self.assertEqual(0, run_evals.run_evaluations(config, runner))
            self.assertTrue(marker.exists())

    def test_run_evaluations_skips_completed_and_records_new_via_recorded_runner(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            output = tmp_path / "out.jsonl"
            output.write_text(
                json.dumps(
                    {
                        "case_id": "direct-answer",
                        "trial": 1,
                        "condition": "baseline",
                        "runner": "recorded",
                        "response": "prior",
                        "usage": {},
                        "cost_usd": 0.5,
                    }
                )
                + "\n"
            )
            config = run_evals.RunConfig(
                cases=ROOT / "evals" / "cases.jsonl",
                runner_config=None,
                runner="recorded",
                condition="baseline",
                condition_skill=None,
                case=["direct-answer", "casual-message"],
                trials=1,
                retries=0,
                budget_usd=1.0,
                allow_unmetered=True,
                output=output,
            )
            runner = self._RecordedRunner(
                [run_evals.Response(text="hi", usage={}, cost_usd=0.1)]
            )

            result = run_evals.run_evaluations(config, runner=runner)

            self.assertEqual(0, result)
            self.assertEqual(1, len(runner.calls))
            prompt, remaining_budget = runner.calls[0]
            self.assertEqual("Thanks, that solved it.", prompt)
            self.assertAlmostEqual(0.5, remaining_budget)

            rows = run_evals.read_jsonl(output)
            self.assertEqual(2, len(rows))
            self.assertEqual("prior", rows[0]["response"])
            self.assertEqual("casual-message", rows[1]["case_id"])
            self.assertEqual("hi", rows[1]["response"])

    class _RecordedRunner(run_evals.Runner):
        """A canned Runner for tests: no subprocess, just plays back responses in order."""

        def __init__(self, responses):
            self._responses = list(responses)
            self.calls = []

        def invoke(self, prompt, *, remaining_budget):
            self.calls.append((prompt, remaining_budget))
            return self._responses.pop(0)

    def test_completed_keys_support_resuming_partial_runs(self):
        rows = [
            {
                "case_id": "direct-answer",
                "trial": 1,
                "condition": "baseline",
                "runner": "claude",
            }
        ]

        self.assertEqual(
            {("direct-answer", 1, "baseline", "claude")},
            run_evals.completed_keys(rows),
        )


class ParseResponseTest(unittest.TestCase):
    def test_extracts_claude_json_fields(self):
        output = json.dumps({"result": "  hi  ", "usage": {"foo": 1}, "total_cost_usd": 0.02})

        text, usage, cost = run_evals._parse_response(output, "claude-json")

        self.assertEqual("hi", text)
        self.assertEqual({"foo": 1}, usage)
        self.assertEqual(0.02, cost)

    def test_extracts_codex_jsonl_fields(self):
        events = [
            {"type": "item.completed", "item": {"type": "agent_message", "text": "  hello  "}},
            {"type": "turn.completed", "usage": {"tokens": 42}},
        ]
        output = "\n".join(json.dumps(event) for event in events)

        text, usage, cost = run_evals._parse_response(output, "codex-jsonl")

        self.assertEqual("hello", text)
        self.assertEqual({"tokens": 42}, usage)
        self.assertIsNone(cost)

    def test_codex_jsonl_ignores_incomplete_events(self):
        events = [
            {"type": "item.completed", "item": {"type": "reasoning", "text": "skip me"}},
            {"type": "item.completed", "item": {"type": "agent_message", "text": "final"}},
        ]
        output = "\n".join(json.dumps(event) for event in events)

        text, usage, cost = run_evals._parse_response(output, "codex-jsonl")

        self.assertEqual("final", text)
        self.assertEqual({}, usage)


class SubprocessRunnerTest(unittest.TestCase):
    """Exercises the runner directly instead of only through run_evaluations,
    so retry/backoff and response parsing are covered without a live provider CLI."""

    def test_retries_until_success_and_sleeps_with_backoff(self):
        with tempfile.TemporaryDirectory() as tmp:
            counter = Path(tmp) / "attempts"
            script = (
                f'n=$(cat {counter} 2>/dev/null || echo 0); n=$((n + 1)); echo "$n" > {counter}; '
                f'if [ "$n" -lt 3 ]; then exit 1; fi; '
                'echo \'{"result": "ok", "total_cost_usd": 0.01}\''
            )
            runner = run_evals.SubprocessRunner(
                {"command": ["sh", "-c", script], "response_format": "claude-json"},
                retries=2,
                allow_unmetered=False,
            )

            with mock.patch("run_evals.time.sleep") as sleep:
                response = runner.invoke("prompt", remaining_budget=1.0)

            self.assertEqual("ok", response.text)
            self.assertEqual(0.01, response.cost_usd)
            self.assertEqual(3, int(counter.read_text().strip()))
            self.assertEqual([mock.call(1), mock.call(2)], sleep.call_args_list)

    def test_raises_after_exhausting_retries(self):
        runner = run_evals.SubprocessRunner(
            {"command": ["sh", "-c", "echo boom 1>&2; exit 1"], "response_format": "text"},
            retries=1,
            allow_unmetered=True,
        )

        with mock.patch("run_evals.time.sleep") as sleep:
            with self.assertRaisesRegex(RuntimeError, "failed after 2 attempts"):
                runner.invoke("prompt", remaining_budget=1.0)

        self.assertEqual(1, sleep.call_count)

    def test_failure_detail_prefers_parsed_response_over_raw_stdout(self):
        output = json.dumps({"result": "explained failure"})
        runner = run_evals.SubprocessRunner(
            {
                "command": ["sh", "-c", f"echo '{output}'; exit 1"],
                "response_format": "claude-json",
            },
            retries=0,
            allow_unmetered=True,
        )

        with self.assertRaisesRegex(RuntimeError, "explained failure"):
            runner.invoke("prompt", remaining_budget=1.0)

    def test_raises_when_claude_json_omits_cost_and_unmetered_not_allowed(self):
        output = json.dumps({"result": "ok"})
        runner = run_evals.SubprocessRunner(
            {"command": ["sh", "-c", f"echo '{output}'"], "response_format": "claude-json"},
            retries=0,
            allow_unmetered=False,
        )

        with self.assertRaisesRegex(RuntimeError, "did not report dollar cost"):
            runner.invoke("prompt", remaining_budget=1.0)


if __name__ == "__main__":
    unittest.main()
