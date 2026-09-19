"""Offline generation-budget regressions; only the provider process is replaced."""

import argparse
import contextlib
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


class GenerationBudgetTest(unittest.TestCase):
    def setUp(self):
        temporary = self.enterContext(tempfile.TemporaryDirectory())
        root = Path(temporary)
        cases = root / "cases.jsonl"
        cases.write_text(json.dumps({
            "id": "probe", "category": "direct-answer", "prompt": "17 * 6?",
            "risk": "low", "criteria": ["Answers 102."],
        }) + "\n", encoding="utf-8")
        runners = root / "runners.json"
        runners.write_text(json.dumps({"stub": {
            "command": ["offline-provider"], "response_format": "claude-json",
            "budget_flag": "--max-budget-usd",
        }}), encoding="utf-8")
        self.args = argparse.Namespace(
            cases=cases, runner_config=runners, runner="stub", condition="baseline",
            condition_skill=None, case=None, trials=1, retries=1, budget_usd=1.0,
            allow_unmetered=False, output=root / "responses.jsonl",
        )
        self.log = self.enterContext(contextlib.redirect_stdout(io.StringIO()))
        self.enterContext(contextlib.redirect_stderr(io.StringIO()))
        self.enterContext(mock.patch.object(run_evals.time, "sleep"))

    @staticmethod
    def result(cost, returncode=0):
        return subprocess.CompletedProcess(
            ["offline-provider"], returncode,
            json.dumps({"type": "result", "subtype": "error_during_execution"
                        if returncode else "success", "is_error": bool(returncode),
                        "result": "paid attempt failed" if returncode else "102",
                        "total_cost_usd": cost, "usage": {}}), "",
        )

    @staticmethod
    def allowances(provider):
        return [call.args[0][call.args[0].index("--max-budget-usd") + 1]
                for call in provider.call_args_list]

    def test_failed_cost_reduces_retry_and_next_trial_allowances(self):
        # Ignoring the first failed call must not grant $1 again on retry.
        self.args.trials = 2
        with mock.patch.object(run_evals.subprocess, "run", side_effect=[
            self.result(0.6, 1), self.result(0.1), self.result(0.1),
        ]) as provider:
            self.assertEqual(0, run_evals.run_evaluations(self.args))
        self.assertEqual(["1.0000", "0.4000", "0.3000"], self.allowances(provider))
        self.assertIn("Reported cost: $0.8000", self.log.getvalue())
        rows = run_evals.read_jsonl(self.args.output)
        self.assertEqual([1, 2], [row["trial"] for row in rows])
        self.assertEqual([0.1, 0.1], [row["cost_usd"] for row in rows])
        self.assertEqual({"case_id", "trial", "condition", "runner", "response",
                          "usage", "cost_usd"}, set(rows[0]))

    def test_failed_only_run_retains_cost_without_completing_answer(self):
        self.args.retries = 0
        with mock.patch.object(run_evals.subprocess, "run", return_value=self.result(0.6, 1)):
            with self.assertRaisesRegex(RuntimeError, "paid attempt failed"):
                run_evals.run_evaluations(self.args)
        self.assertEqual([], run_evals.read_jsonl(self.args.output))
        with mock.patch.object(run_evals.subprocess, "run", return_value=self.result(0.1)) as provider:
            self.assertEqual(0, run_evals.run_evaluations(self.args))
        self.assertEqual(["0.4000"], self.allowances(provider))
        self.assertEqual(["102"], [row["response"] for row in run_evals.read_jsonl(self.args.output)])

    def test_resume_counts_failed_and_successful_attempts_once(self):
        with mock.patch.object(run_evals.subprocess, "run", side_effect=[
            self.result(0.6, 1), self.result(0.1),
        ]):
            self.assertEqual(0, run_evals.run_evaluations(self.args))
        self.args.trials = 2
        with mock.patch.object(run_evals.subprocess, "run", return_value=self.result(0.1)) as provider:
            self.assertEqual(0, run_evals.run_evaluations(self.args))
        self.assertEqual(["0.3000"], self.allowances(provider))
        self.assertEqual([1, 2], [row["trial"] for row in run_evals.read_jsonl(self.args.output)])

    def test_exhausted_failed_attempt_prevents_retry_and_resume(self):
        with mock.patch.object(run_evals.subprocess, "run", side_effect=[
            self.result(1.0, 1), self.result(0.1),
        ]) as provider:
            self.assertEqual(2, run_evals.run_evaluations(self.args))
            self.assertEqual(1, provider.call_count)
        with mock.patch.object(run_evals.subprocess, "run") as provider:
            self.assertEqual(2, run_evals.run_evaluations(self.args))
            provider.assert_not_called()
        self.assertEqual([], run_evals.read_jsonl(self.args.output))

    def test_unknown_or_invalid_failed_cost_stops_retry_and_metered_resume(self):
        for cost in (None, -0.1, True, "0.1", float("nan"), float("inf")):
            with self.subTest(cost=cost):
                self.args.output = self.args.output.with_name(f"cost-{repr(cost)}.jsonl")
                with mock.patch.object(run_evals.subprocess, "run", return_value=self.result(cost, 1)) as provider:
                    with self.assertRaisesRegex(RuntimeError, "cost"):
                        run_evals.run_evaluations(self.args)
                    self.assertEqual(1, provider.call_count)
                self.assertEqual([], run_evals.read_jsonl(self.args.output))
                with mock.patch.object(run_evals.subprocess, "run", return_value=self.result(0.1)) as provider:
                    with self.assertRaisesRegex(RuntimeError, "cost"):
                        run_evals.run_evaluations(self.args)
                    provider.assert_not_called()

    def test_unparseable_failure_blocks_metered_resume(self):
        bad_result = subprocess.CompletedProcess([], 1, "not JSON", "runner interrupted")
        with mock.patch.object(run_evals.subprocess, "run", return_value=bad_result) as provider:
            with self.assertRaisesRegex(RuntimeError, "cost"):
                run_evals.run_evaluations(self.args)
            self.assertEqual(1, provider.call_count)
        with mock.patch.object(run_evals.subprocess, "run") as provider:
            with self.assertRaisesRegex(RuntimeError, "cost"):
                run_evals.run_evaluations(self.args)
            provider.assert_not_called()

    def test_invalid_success_cost_is_not_a_completed_answer(self):
        for cost in (None, -0.1, False, "0.1", float("nan"), float("inf")):
            with self.subTest(cost=cost):
                self.args.output = self.args.output.with_name(f"success-{repr(cost)}.jsonl")
                with mock.patch.object(run_evals.subprocess, "run", return_value=self.result(cost)):
                    with self.assertRaisesRegex(RuntimeError, "cost"):
                        run_evals.run_evaluations(self.args)
                self.assertEqual([], run_evals.read_jsonl(self.args.output))
                with mock.patch.object(run_evals.subprocess, "run", return_value=self.result(0.1)) as provider:
                    with self.assertRaisesRegex(RuntimeError, "cost"):
                        run_evals.run_evaluations(self.args)
                    provider.assert_not_called()

    def test_allow_unmetered_explicitly_permits_unknown_failed_cost(self):
        self.args.allow_unmetered = True
        with mock.patch.object(run_evals.subprocess, "run", side_effect=[
            self.result(None, 1), self.result(None),
        ]) as provider:
            self.assertEqual(0, run_evals.run_evaluations(self.args))
        self.assertEqual(["1.0000", "1.0000"], self.allowances(provider))
        self.assertIsNone(run_evals.read_jsonl(self.args.output)[0]["cost_usd"])
        self.args.trials = 2
        with mock.patch.object(run_evals.subprocess, "run", return_value=self.result(0)) as provider:
            self.assertEqual(0, run_evals.run_evaluations(self.args))
        self.assertEqual(["1.0000"], self.allowances(provider))

    def test_allow_unmetered_still_charges_known_failed_cost(self):
        self.args.allow_unmetered = True
        with mock.patch.object(run_evals.subprocess, "run", side_effect=[
            self.result(0.6, 1), self.result(None),
        ]) as provider:
            self.assertEqual(0, run_evals.run_evaluations(self.args))
        self.assertEqual(["1.0000", "0.4000"], self.allowances(provider))

    def test_zero_failed_cost_allows_retry(self):
        with mock.patch.object(run_evals.subprocess, "run", side_effect=[
            self.result(0, 1), self.result(0.1),
        ]) as provider:
            self.assertEqual(0, run_evals.run_evaluations(self.args))
        self.assertEqual(["1.0000", "1.0000"], self.allowances(provider))

    def test_retry_allowance_rounds_down_and_stops_below_precision(self):
        self.args.retries = 2
        with mock.patch.object(run_evals.subprocess, "run", side_effect=[
            self.result(0.60004, 1), self.result(0.39991, 1), self.result(0),
        ]) as provider:
            self.assertEqual(2, run_evals.run_evaluations(self.args))
        self.assertEqual(["1.0000", "0.3999"], self.allowances(provider))

    def test_failed_cost_is_scoped_to_condition_and_runner(self):
        self.args.retries = 0
        with mock.patch.object(run_evals.subprocess, "run", return_value=self.result(0.6, 1)):
            with self.assertRaises(RuntimeError):
                run_evals.run_evaluations(self.args)
        runners = json.loads(self.args.runner_config.read_text(encoding="utf-8"))
        runners["other"] = runners["stub"]
        self.args.runner_config.write_text(json.dumps(runners), encoding="utf-8")
        self.args.runner = "other"
        with mock.patch.object(run_evals.subprocess, "run", return_value=self.result(0.1)) as provider:
            self.assertEqual(0, run_evals.run_evaluations(self.args))
        self.assertEqual(["1.0000"], self.allowances(provider))
        self.args.runner = "stub"
        self.args.condition = "candidate"
        self.args.condition_skill = ROOT / "skills/i-have-adhd/SKILL.md"
        with mock.patch.object(run_evals.subprocess, "run", return_value=self.result(0.1)) as provider:
            self.assertEqual(0, run_evals.run_evaluations(self.args))
        self.assertEqual(["1.0000"], self.allowances(provider))
        self.args.condition = "baseline"
        with mock.patch.object(run_evals.subprocess, "run", return_value=self.result(0.1)) as provider:
            self.assertEqual(0, run_evals.run_evaluations(self.args))
        self.assertEqual(["0.4000"], self.allowances(provider))

    def test_legacy_invalid_or_missing_cost_blocks_metered_resume(self):
        for cost in (None, -0.1, True, "0.1", float("nan"), float("inf")):
            with self.subTest(cost=cost):
                self.args.output.write_text(json.dumps({
                    "case_id": "probe", "trial": 1, "condition": "baseline",
                    "runner": "stub", "response": "102", "cost_usd": cost,
                }) + "\n", encoding="utf-8")
                self.args.trials = 2
                with mock.patch.object(run_evals.subprocess, "run", return_value=self.result(0.1)) as provider:
                    with self.assertRaisesRegex(RuntimeError, "cost"):
                        run_evals.run_evaluations(self.args)
                    provider.assert_not_called()


if __name__ == "__main__":
    unittest.main()
