import argparse
from contextlib import redirect_stdout
import io
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
            args.budget_usd = None
            captured = io.StringIO()
            with redirect_stdout(captured):
                self.assertEqual(0, run_evals.run_evaluations(args))
            self.assertTrue(marker.exists())
            self.assertIn("Reported cost: unavailable", captured.getvalue())

    def test_unmetered_runner_rejects_an_explicit_budget_before_any_call(self):
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
                budget_usd=5.0,
                allow_unmetered=True,
                output=tmp_path / "out.jsonl",
            )

            with self.assertRaisesRegex(RuntimeError, "cannot be enforced"):
                run_evals.run_evaluations(args)

            self.assertFalse(marker.exists(), "runner was invoked before the rejection")
            self.assertFalse((tmp_path / "out.jsonl").exists())

    def test_metered_runner_keeps_the_default_budget(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            runner_config = tmp_path / "runners.json"
            runner_config.write_text(
                json.dumps(
                    {
                        "stub": {
                            "command": ["stub-runner"],
                            "response_format": "claude-json",
                            "budget_flag": "--max-budget-usd",
                        }
                    }
                ),
                encoding="utf-8",
            )
            output = tmp_path / "responses.jsonl"
            args = run_evals._build_parser().parse_args(
                [
                    "run",
                    "--runner-config",
                    str(runner_config),
                    "--runner",
                    "stub",
                    "--condition",
                    "baseline",
                    "--case",
                    "direct-answer",
                    "--trials",
                    "1",
                    "--retries",
                    "0",
                    "--output",
                    str(output),
                ]
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
                self.assertEqual(0, run_evals.run_evaluations(args))

            self.assertIsNone(args.budget_usd)
            self.assertEqual(
                ["--max-budget-usd", "25.0000"],
                runner.call_args.args[0][1:3],
            )

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
                budget_usd=None,
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
