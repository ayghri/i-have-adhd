import argparse
import json
import sys
import tempfile
import unittest
from pathlib import Path


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

    def test_usage_summary_reports_token_and_cost_deltas(self):
        rows = [
            self._usage_row(
                "direct-answer",
                "baseline",
                "abcdefghij",
                1.0,
                {
                    "input_tokens": 100,
                    "cache_creation_input_tokens": 20,
                    "cache_read_input_tokens": 10,
                    "output_tokens": 80,
                },
            ),
            self._usage_row(
                "medical-boundary",
                "baseline",
                "abcdef",
                0.5,
                {"input_tokens": 50, "output_tokens": 20},
            ),
            self._usage_row(
                "direct-answer",
                "candidate",
                "abcd",
                0.6,
                {"input_tokens": 110, "cached_input_tokens": 10, "output_tokens": 40},
            ),
            self._usage_row(
                "medical-boundary",
                "candidate",
                "wxyz",
                0.3,
                {"input_tokens": 40, "output_tokens": 10},
            ),
        ]

        summary = run_evals.summarize_usage(rows)

        self.assertEqual("claude", summary["runner"])
        self.assertEqual(180, summary["conditions"]["baseline"]["input_tokens"])
        self.assertEqual(50, summary["conditions"]["candidate"]["output_tokens"])
        self.assertAlmostEqual(25.0, summary["conditions"]["candidate"]["mean_output_tokens"])
        self.assertEqual(-50, summary["delta"]["candidate"]["output_tokens"])
        self.assertAlmostEqual(-50.0, summary["delta"]["candidate"]["output_tokens_pct"])
        self.assertAlmostEqual(-0.6, summary["delta"]["candidate"]["cost_usd"])
        self.assertAlmostEqual(-40.0, summary["delta"]["candidate"]["cost_usd_pct"])
        self.assertAlmostEqual(
            -50.0, summary["delta"]["candidate"]["mean_response_chars_pct"]
        )

    def test_usage_summary_rejects_mixed_runners(self):
        rows = [
            self._usage_row("direct-answer", "baseline", "a", 0.1, {}, runner="claude"),
            self._usage_row("direct-answer", "candidate", "b", None, {}, runner="codex"),
        ]

        with self.assertRaisesRegex(ValueError, "claude.*codex"):
            run_evals.summarize_usage(rows)

    def test_usage_summary_rejects_unpaired_conditions(self):
        rows = [
            self._usage_row("direct-answer", "baseline", "a", 0.1, {}),
            self._usage_row("medical-boundary", "baseline", "b", 0.1, {}),
            self._usage_row("direct-answer", "candidate", "c", 0.1, {}),
        ]

        with self.assertRaisesRegex(ValueError, "not judged on the same rows"):
            run_evals.summarize_usage(rows)

    def test_usage_summary_marks_unreported_cost(self):
        rows = [
            self._usage_row("direct-answer", "baseline", "a", 0.1, {}),
            self._usage_row("direct-answer", "candidate", "b", None, {}),
        ]

        summary = run_evals.summarize_usage(rows)

        candidate = summary["conditions"]["candidate"]
        self.assertIsNone(candidate["input_tokens"])
        self.assertIsNone(candidate["output_tokens"])
        self.assertIsNone(candidate["cost_usd"])
        self.assertEqual(1, candidate["cost_usd_unreported_rows"])
        self.assertIsNone(summary["delta"]["candidate"]["cost_usd"])
        self.assertIsNone(summary["delta"]["candidate"]["cost_usd_pct"])

    def test_usage_tokens_handles_both_runner_shapes(self):
        self.assertEqual(
            (15, 4),
            run_evals._usage_tokens(
                {
                    "input_tokens": 10,
                    "cache_creation_input_tokens": 2,
                    "cache_read_input_tokens": 3,
                    "output_tokens": 4,
                }
            ),
        )
        self.assertEqual(
            (12, 7),
            run_evals._usage_tokens(
                {"input_tokens": 12, "cached_input_tokens": 5, "output_tokens": 7}
            ),
        )
        self.assertEqual((None, None), run_evals._usage_tokens({}))

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

    @staticmethod
    def _usage_row(case_id, condition, response, cost, usage, runner="claude", trial=1):
        return {
            "case_id": case_id,
            "trial": trial,
            "condition": condition,
            "runner": runner,
            "response": response,
            "usage": usage,
            "cost_usd": cost,
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
