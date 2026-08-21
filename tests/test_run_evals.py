import argparse
import json
import subprocess
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


    def test_parse_response_tolerates_output_after_the_json_document(self):
        """The CLI can emit a notice after its JSON result; the first document still wins."""
        payload = json.dumps(
            {"result": "102", "usage": {"input_tokens": 2}, "total_cost_usd": 0.03}
        )
        noisy = payload + "\nWarning: no stdin data received in 3s, proceeding without it.\n"

        text, usage, cost = run_evals._parse_response(noisy, "claude-json")

        self.assertEqual("102", text)
        self.assertEqual({"input_tokens": 2}, usage)
        self.assertAlmostEqual(0.03, cost)

    def test_runner_invocation_closes_child_stdin(self):
        """A runner that inherits stdin can read unrelated bytes into the prompt."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cases = root / "cases.jsonl"
            cases.write_text(
                json.dumps(
                    {
                        "id": "probe",
                        "category": "direct-answer",
                        "prompt": "What is 17 multiplied by 6?",
                        "risk": "low",
                        "criteria": ["Answers 102."],
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            runners = root / "runners.json"
            runners.write_text(
                json.dumps(
                    {
                        "stub": {
                            "command": ["stub-runner"],
                            "response_format": "claude-json",
                        }
                    }
                ),
                encoding="utf-8",
            )
            output = root / "responses.jsonl"
            args = argparse.Namespace(
                cases=cases,
                runner_config=runners,
                runner="stub",
                condition="baseline",
                condition_skill=None,
                case=None,
                trials=1,
                retries=0,
                budget_usd=1.0,
                allow_unmetered=False,
                output=output,
            )
            completed = subprocess.CompletedProcess(
                args=["stub-runner"],
                returncode=0,
                stdout=json.dumps({"result": "102", "usage": {}, "total_cost_usd": 0.01}),
                stderr="",
            )

            with mock.patch.object(
                run_evals.subprocess, "run", return_value=completed
            ) as runner:
                run_evals.run_evaluations(args)

            self.assertEqual(1, runner.call_count)
            self.assertIs(subprocess.DEVNULL, runner.call_args.kwargs.get("stdin"))

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
                            "command": [
                                sys.executable,
                                "-c",
                                f"from pathlib import Path; Path({str(marker)!r}).touch(); print('hi')",
                            ],
                            "response_format": "text",
                        }
                    }
                )
            )
            args = argparse.Namespace(
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
                run_evals.run_evaluations(args)

            self.assertFalse(marker.exists(), "runner was invoked before the rejection")
            self.assertFalse((tmp_path / "out.jsonl").exists())

            args.allow_unmetered = True
            self.assertEqual(0, run_evals.run_evaluations(args))
            self.assertTrue(marker.exists())

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


if __name__ == "__main__":
    unittest.main()
