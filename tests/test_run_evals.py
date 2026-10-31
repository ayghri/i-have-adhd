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

    def test_usage_rejects_invalid_measurements(self):
        for cost in (-1, True, False, float("nan"), float("inf"), "0.1"):
            with self.subTest(cost=cost):
                rows = [self._usage_row("a", condition, "ok", cost, {})
                        for condition in ("baseline", "candidate")]
                with self.assertRaisesRegex(ValueError, "cost_usd"):
                    run_evals.summarize_usage(rows)
        for key in ("input_tokens", "output_tokens", "cache_creation_input_tokens",
                    "cache_read_input_tokens", "cached_input_tokens"):
            for value in (-1, True, 1.5, float("nan"), "10"):
                with self.subTest(key=key, value=value):
                    with self.assertRaisesRegex(ValueError, key):
                        run_evals._usage_tokens({key: value})
        with self.assertRaisesRegex(ValueError, "usage"):
            run_evals._usage_tokens([])

    def test_usage_rejects_overflowing_cost_total(self):
        rows = [self._usage_row(case, condition, "ok", 1e308, {})
                for case in ("a", "b") for condition in ("baseline", "candidate")]
        with self.assertRaisesRegex(ValueError, "cost total is not finite"):
            run_evals.summarize_usage(rows)

    def test_usage_distinguishes_missing_counts_from_zero(self):
        self.assertEqual((None, None), run_evals._usage_tokens(None))
        self.assertEqual((None, 2), run_evals._usage_tokens(
            {"cache_read_input_tokens": 10, "output_tokens": 2}))
        self.assertEqual((None, 2), run_evals._usage_tokens(
            {"input_tokens": 10, "cache_read_input_tokens": None, "output_tokens": 2}))
        rows = [self._usage_row("a", condition, "", 0,
                               {"input_tokens": 0, "output_tokens": 0})
                for condition in ("baseline", "candidate")]
        result = run_evals.summarize_usage(rows)
        self.assertEqual(0, result["conditions"]["candidate"]["input_tokens"])
        self.assertEqual(0, result["delta"]["candidate"]["cost_usd"])
        self.assertIsNone(result["delta"]["candidate"]["cost_usd_pct"])
        rows[1]["usage"] = None
        self.assertIsNone(run_evals.summarize_usage(rows)["delta"]["candidate"]["input_tokens"])

    def test_usage_rejects_duplicate_or_invalid_rows(self):
        rows = [self._usage_row("a", condition, "ok", 0, {})
                for condition in ("baseline", "candidate")]
        with self.assertRaisesRegex(ValueError, "duplicate"):
            run_evals.summarize_usage(rows + [rows[0]])
        for field, value in (("condition", "unknown"), ("case_id", None),
                             ("trial", True), ("trial", 0), ("runner", ""),
                             ("response", None)):
            with self.subTest(field=field):
                invalid = [dict(rows[0]), dict(rows[1])]
                invalid[1][field] = value
                with self.assertRaises(ValueError):
                    run_evals.summarize_usage(invalid)

    def test_usage_checks_model_metadata_when_available(self):
        rows = [self._usage_row("a", condition, "ok", 0, {})
                for condition in ("baseline", "candidate")]
        self.assertIsNone(run_evals.summarize_usage(rows)["model"])
        rows[0]["model"] = "model-a"
        with self.assertRaisesRegex(ValueError, "same model"):
            run_evals.summarize_usage(rows)
        rows[1]["model"] = "model-b"
        with self.assertRaisesRegex(ValueError, "same model"):
            run_evals.summarize_usage(rows)
        rows[1]["model"] = "model-a"
        self.assertEqual("model-a", run_evals.summarize_usage(rows)["model"])

    def test_measure_cli_reports_increased_input_and_cost(self):
        rows = [
            self._usage_row("a", "baseline", "long answer", 0.1,
                            {"input_tokens": 100, "output_tokens": 20}),
            self._usage_row("a", "candidate", "short", 0.15,
                            {"input_tokens": 150, "output_tokens": 10}),
        ]
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "responses.jsonl"
            contents = "".join(json.dumps(row) + "\n" for row in rows)
            path.write_text(contents, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/run_evals.py"), "measure", str(path)],
                check=True, capture_output=True, text=True, timeout=10,
            )
            self.assertEqual(contents, path.read_text(encoding="utf-8"))
        delta = json.loads(result.stdout)["delta"]["candidate"]
        self.assertEqual(50, delta["input_tokens"])
        self.assertEqual(50, delta["input_tokens_pct"])
        self.assertEqual(-50, delta["output_tokens_pct"])
        self.assertAlmostEqual(50, delta["cost_usd_pct"])

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

    def test_condition_prompt_injects_the_skill_body_without_frontmatter(self):
        # hooks/always-on.sh strips the YAML frontmatter before injecting the
        # ruleset, so the eval must grade the same text that actually ships.
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp) / "SKILL.md"
            skill.write_text(
                "---\n"
                "name: i-have-adhd\n"
                "disable-model-invocation: true\n"
                "metadata:\n"
                "  hermes:\n"
                "    tags: [ADHD]\n"
                "---\n"
                "\n"
                "# i-have-adhd\n"
                "\n"
                "Lead with the next action.\n"
            )

            prompt = run_evals._condition_prompt("Fix the bug.", "candidate", skill)

            self.assertIn("Lead with the next action.", prompt)
            self.assertIn("Fix the bug.", prompt)
            self.assertNotIn("disable-model-invocation", prompt)
            self.assertNotIn("hermes", prompt)

    def test_condition_prompt_keeps_a_skill_body_that_has_no_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp) / "SKILL.md"
            skill.write_text("# No frontmatter here\n\nLead with the next action.\n")

            prompt = run_evals._condition_prompt("Fix the bug.", "candidate", skill)

            self.assertIn("# No frontmatter here", prompt)

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

    def test_generation_runs_outside_the_repository(self):
        # An agent CLI adopts its working directory as project context. Run it
        # in this checkout and it answers prompts by inspecting the harness,
        # which contaminates the responses being compared.
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            runner_config = tmp_path / "runners.json"
            runner_config.write_text(
                json.dumps({"pwd": {"command": ["sh", "-c", "pwd"], "response_format": "text"}})
            )
            output = tmp_path / "out.jsonl"
            args = argparse.Namespace(
                cases=ROOT / "evals" / "cases.jsonl",
                runner_config=runner_config,
                runner="pwd",
                condition="baseline",
                condition_skill=None,
                case=["direct-answer"],
                trials=1,
                retries=0,
                budget_usd=1.0,
                allow_unmetered=True,
                output=output,
            )

            self.assertEqual(0, run_evals.run_evaluations(args))

            where = Path(run_evals.read_jsonl(output)[0]["response"].strip()).resolve()
            self.assertNotEqual(ROOT.resolve(), where)
            self.assertFalse(str(where).startswith(str(ROOT.resolve())))

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
