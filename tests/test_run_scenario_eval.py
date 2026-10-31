"""Offline checks for session capture and compatibility with paired judging."""

import argparse
import contextlib
import io
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import judge
import run_evals
import run_scenario_eval

SCENARIO = ROOT / "evals/scenarios/persistence-topic-switch-stop"


class ScenarioEvaluationTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = pathlib.Path(temporary.name)
        self.args = argparse.Namespace(
            scenario=SCENARIO, condition="candidate",
            condition_skill=ROOT / "skills/i-have-adhd/SKILL.md",
            model="fixture", budget_usd=1.0, trial=1,
            output=self.root / "response.jsonl",
        )

    def run_capture(self):
        with contextlib.redirect_stdout(io.StringIO()):
            run_scenario_eval.run_scenario(self.args)
        return run_evals.read_jsonl(self.args.output)[0]

    def test_invalid_turns_are_rejected(self):
        original = run_scenario_eval.load_scenario(SCENARIO)
        self.assertEqual(6, len(original["turns"]))
        for turns in ([], [None, None], [{"id": "a", "prompt": ""}] * 2,
                      [{"id": "a", "prompt": "task"}] * 2):
            with self.subTest(turns=turns):
                case = dict(original, turns=turns)
                (self.root / "case.jsonl").write_text(json.dumps(case) + "\n")
                with self.assertRaises(ValueError):
                    run_scenario_eval.load_scenario(self.root)

    @mock.patch("run_scenario_eval.subprocess.run")
    def test_capture_is_compatible_with_existing_blind_judge(self, run):
        run.return_value = subprocess.CompletedProcess(
            [], 0, json.dumps({"result": "fixture response", "total_cost_usd": 0.01}), ""
        )
        candidate = self.run_capture()
        calls = run.call_args_list
        commands = [call.args[0] for call in calls]
        session_id = commands[0][commands[0].index("--session-id") + 1]
        self.assertEqual(6, len(commands))
        self.assertIn("<response_style>", commands[0][-1])
        self.assertNotIn("disable-model-invocation:", commands[0][-1])
        for command in commands[1:]:
            self.assertEqual(session_id, command[command.index("--resume") + 1])
            self.assertNotIn("<response_style>", command[-1])
        self.assertEqual(1, len({call.kwargs["cwd"] for call in calls}))
        for call in calls:
            self.assertNotEqual(str(ROOT), call.kwargs["cwd"])
            self.assertEqual(subprocess.DEVNULL, call.kwargs["stdin"])
            self.assertIn("--safe-mode", call.args[0])
            self.assertIn("--strict-mcp-config", call.args[0])
            command = call.args[0]
            self.assertEqual("", command[command.index("--tools") + 1])
        self.assertEqual("0.950000", commands[-1][-2])
        self.assertAlmostEqual(0.06, candidate["cost_usd"])

        self.args.condition = "baseline"
        self.args.output = self.root / "baseline.jsonl"
        run.reset_mock()
        baseline = self.run_capture()
        self.assertNotIn("response_style", run.call_args_list[0].args[0][-1])
        self.assertEqual(baseline["response"], candidate["response"])
        groups = judge.group_responses([baseline, candidate])
        key = (SCENARIO.name, 1)
        labels = judge.assign_labels(key, list(groups[key]))
        prompt = judge.build_judge_prompt(
            run_scenario_eval.load_scenario(SCENARIO), groups[key], labels,
            judge.grader_rubric((ROOT / "evals/rubric.md").read_text()),
        )
        for hidden in ("baseline", "candidate", session_id, "response_style"):
            self.assertNotIn(hidden, prompt)
        verdict = {label: dict.fromkeys(judge.DIMENSIONS, 4) | {
            "blocker": False, "notes": "fixture only"
        } for label in labels.values()}
        scores = judge.parse_judge_scores(json.dumps(verdict), key, labels)
        self.assertEqual(2, len(scores))
        self.assertFalse(run_evals.summarize_scores(scores)["release_gate"]["passed"])

    @mock.patch("run_scenario_eval.subprocess.run")
    def test_failed_capture_cannot_be_judged_as_complete(self, run):
        for payload, returncode, message in (
            ({"total_cost_usd": 0.12}, 0, "0.130000"),
            ({"result": "error", "total_cost_usd": 0.12}, 1, "0.130000"),
            ({"is_error": True, "result": "error", "total_cost_usd": 0.12}, 0, "0.130000"),
            ({"result": "ok", "total_cost_usd": 2}, 0, "Budget exceeded"),
        ):
            with self.subTest(payload=payload, returncode=returncode):
                self.args.output = self.root / f"failed-{returncode}-{message}-{len(payload)}.jsonl"
                run.side_effect = [
                    subprocess.CompletedProcess([], 0, '{"result":"ok","total_cost_usd":0.01}', ""),
                    subprocess.CompletedProcess([], returncode, json.dumps(payload), ""),
                ]
                with self.assertRaisesRegex(RuntimeError, message):
                    self.run_capture()
                self.assertEqual([], run_evals.read_jsonl(self.args.output))

    @mock.patch("run_scenario_eval.subprocess.run")
    def test_invalid_costs_and_payloads_fail_closed(self, run):
        payloads = [[], None, "error"] + [
            {"result": "ok", "total_cost_usd": cost}
            for cost in (True, False, float("nan"), float("inf"), -1, None, "0.1")
        ]
        for payload in payloads:
            with self.subTest(payload=payload):
                run.return_value = subprocess.CompletedProcess([], 0, json.dumps(payload), "")
                with self.assertRaisesRegex(RuntimeError, "call cost unavailable"):
                    run_scenario_eval.call_claude([], str(self.root), 0.1)

    @mock.patch("run_scenario_eval.subprocess.run")
    def test_invalid_inputs_and_existing_output_do_not_start_provider(self, run):
        for budget in (0, -1, 26, float("nan"), float("inf")):
            self.args.budget_usd = budget
            with self.assertRaises(ValueError):
                self.run_capture()
        self.args.budget_usd = 1
        self.args.output.write_text("existing results")
        with self.assertRaises(FileExistsError):
            self.run_capture()
        self.assertEqual("existing results", self.args.output.read_text())
        run.assert_not_called()

    @mock.patch("run_scenario_eval.subprocess.run")
    def test_remaining_budget_is_rounded_down_and_stops_further_calls(self, run):
        self.args.budget_usd = 0.1234569
        run.return_value = subprocess.CompletedProcess(
            [], 0, '{"result":"ok","total_cost_usd":0.123456}', ""
        )
        with self.assertRaisesRegex(RuntimeError, "Budget exhausted"):
            self.run_capture()
        run.assert_called_once()
        self.assertEqual("0.123456", run.call_args.args[0][-2])
        self.assertEqual([], run_evals.read_jsonl(self.args.output))

    def test_actual_child_gets_no_inherited_input_and_times_out(self):
        cli = "import json, sys; print(json.dumps({'result': repr(sys.stdin.read()), 'total_cost_usd': 0}))"
        wrapper = (
            "import sys; sys.path.insert(0, sys.argv[1]); import run_scenario_eval as r; "
            "print(r.call_claude([sys.executable, '-c', sys.argv[2]], sys.argv[3], 0))"
        )
        result = subprocess.run(
            [sys.executable, "-c", wrapper, str(ROOT / "scripts"), cli, str(self.root)],
            input="unrelated parent input", text=True, capture_output=True,
            timeout=5, check=True,
        )
        self.assertIn("''", result.stdout)
        self.assertNotIn("unrelated parent input", result.stdout)
        with mock.patch.object(run_scenario_eval, "CALL_TIMEOUT_SECONDS", 0.1):
            with self.assertRaisesRegex(RuntimeError, "timed out.*0.100000"):
                run_scenario_eval.call_claude(
                    [sys.executable, "-c", "import time; time.sleep(5)"], str(self.root), 0.1
                )


if __name__ == "__main__":
    unittest.main()
