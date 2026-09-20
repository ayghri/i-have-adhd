import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import judge  # noqa: E402
import run_evals  # noqa: E402


class LabelAssignmentTest(unittest.TestCase):
    def test_labels_are_a_stable_bijection_over_conditions(self):
        conditions = ["baseline", "candidate"]

        first = judge.assign_labels(("direct-answer", 1), conditions)
        second = judge.assign_labels(("direct-answer", 1), conditions)

        self.assertEqual(first, second)
        self.assertEqual(sorted(conditions), sorted(first))
        self.assertEqual({"A", "B"}, set(first.values()))

    def test_labels_vary_across_groups_so_position_never_leaks_condition(self):
        conditions = ["baseline", "candidate"]

        seen = {
            judge.assign_labels(("direct-answer", trial), conditions)["baseline"]
            for trial in range(20)
        }

        self.assertEqual({"A", "B"}, seen)


class GroupingTest(unittest.TestCase):
    def test_responses_group_by_case_and_trial(self):
        rows = [
            {"case_id": "direct-answer", "trial": 1, "condition": "baseline", "response": "51"},
            {"case_id": "direct-answer", "trial": 1, "condition": "candidate", "response": "102"},
            {"case_id": "direct-answer", "trial": 2, "condition": "baseline", "response": "again"},
        ]

        groups = judge.group_responses(rows)

        self.assertEqual({"baseline": "51", "candidate": "102"}, groups[("direct-answer", 1)])
        self.assertEqual({"baseline": "again"}, groups[("direct-answer", 2)])

    def test_groups_missing_a_condition_are_partitioned_out_not_dropped(self):
        groups = {
            ("direct-answer", 1): {"baseline": "x", "candidate": "y"},
            ("casual-message", 1): {"baseline": "only one condition ran"},
        }

        complete, incomplete = judge.partition_groups(groups, {"baseline", "candidate"})

        self.assertEqual([("direct-answer", 1)], sorted(complete))
        self.assertEqual([("casual-message", 1)], sorted(incomplete))


class ParseJudgeScoresTest(unittest.TestCase):
    @staticmethod
    def _verdict(value, blocker=False, notes="fixture"):
        return {
            "correctness": value,
            "autonomy": value,
            "actionability": value,
            "safety": value,
            "concision": value,
            "blocker": blocker,
            "notes": notes,
        }

    def test_labels_are_mapped_back_to_their_conditions(self):
        payload = json.dumps({"A": self._verdict(5), "B": self._verdict(2, blocker=True)})

        rows = judge.parse_judge_scores(
            payload, ("direct-answer", 1), {"baseline": "B", "candidate": "A"}
        )

        by_condition = {row["condition"]: row for row in rows}
        self.assertEqual(5, by_condition["candidate"]["correctness"])
        self.assertEqual(2, by_condition["baseline"]["correctness"])
        self.assertTrue(by_condition["baseline"]["blocker"])
        self.assertEqual("direct-answer", by_condition["candidate"]["case_id"])
        self.assertEqual(1, by_condition["candidate"]["trial"])

    def test_out_of_range_score_names_the_case_it_came_from(self):
        payload = json.dumps({"A": self._verdict(9), "B": self._verdict(3)})

        with self.assertRaisesRegex(ValueError, "direct-answer"):
            judge.parse_judge_scores(
                payload, ("direct-answer", 1), {"baseline": "B", "candidate": "A"}
            )

    def test_json_wrapped_in_code_fences_is_still_parsed(self):
        payload = "```json\n" + json.dumps({"A": self._verdict(4), "B": self._verdict(4)}) + "\n```"

        rows = judge.parse_judge_scores(
            payload, ("direct-answer", 1), {"baseline": "B", "candidate": "A"}
        )

        self.assertEqual({"baseline", "candidate"}, {row["condition"] for row in rows})

    def test_missing_label_names_the_label_the_judge_skipped(self):
        payload = json.dumps({"A": self._verdict(4)})

        with self.assertRaisesRegex(ValueError, "B"):
            judge.parse_judge_scores(
                payload, ("direct-answer", 1), {"baseline": "B", "candidate": "A"}
            )


class GraderRubricTest(unittest.TestCase):
    def test_only_the_marked_grader_section_is_extracted(self):
        rubric = (
            "# Response quality rubric\n"
            "<!-- judge:begin -->\n"
            "Score each dimension 1-5.\n"
            "<!-- judge:end -->\n"
            "Release the candidate only when it beats baseline.\n"
        )

        self.assertEqual("Score each dimension 1-5.", judge.grader_rubric(rubric))

    def test_rubric_without_markers_is_used_whole(self):
        self.assertEqual("everything", judge.grader_rubric("everything\n"))

    def test_shipped_rubric_grader_section_never_names_a_condition(self):
        shipped = (ROOT / "evals" / "rubric.md").read_text(encoding="utf-8")

        section = judge.grader_rubric(shipped).lower()

        self.assertNotIn("baseline", section)
        self.assertNotIn("candidate", section)
        self.assertIn("correctness", section)


class PromptTest(unittest.TestCase):
    CASE = {
        "id": "direct-answer",
        "prompt": "What is 17 multiplied by 6?",
        "criteria": ["States 102."],
        "risk": "low",
    }

    def test_prompt_carries_responses_under_labels_and_never_names_conditions(self):
        responses = {"baseline": "Great question! The answer is 102.", "candidate": "102"}
        labels = {"baseline": "B", "candidate": "A"}

        prompt = judge.build_judge_prompt(self.CASE, responses, labels, "SCORE 1-5 PER DIMENSION")

        self.assertIn("Great question! The answer is 102.", prompt)
        self.assertIn("SCORE 1-5 PER DIMENSION", prompt)
        self.assertIn("States 102.", prompt)
        self.assertNotIn("baseline", prompt.lower())
        self.assertNotIn("candidate", prompt.lower())


class NeutralWorkingDirectoryTest(unittest.TestCase):
    def test_runner_cwd_is_fresh_and_outside_the_repository(self):
        # An agent CLI adopts its working directory as project context. Run it
        # in the repo and it starts inspecting the eval harness instead of
        # answering the prompt, which contaminates the responses being graded.
        with run_evals._neutral_cwd() as first:
            cwd = Path(first).resolve()
            self.assertNotEqual(judge.ROOT.resolve(), cwd)
            self.assertFalse(str(cwd).startswith(str(judge.ROOT.resolve())))
            self.assertEqual([], list(cwd.iterdir()))
            (cwd / "state-from-prior-run").write_text("not reusable")

        with run_evals._neutral_cwd() as second:
            next_cwd = Path(second).resolve()
            self.assertNotEqual(cwd, next_cwd)
            self.assertEqual([], list(next_cwd.iterdir()))


class EndToEndTest(unittest.TestCase):
    VERDICT = {
        "correctness": 4,
        "autonomy": 4,
        "actionability": 4,
        "safety": 5,
        "concision": 3,
        "blocker": False,
        "notes": "fixture",
    }

    def test_judging_produces_paired_rows_the_scorer_accepts(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            responses = tmp_path / "responses.jsonl"
            responses.write_text(
                "".join(
                    json.dumps(row) + "\n"
                    for row in (
                        {
                            "case_id": "direct-answer",
                            "trial": 1,
                            "condition": "baseline",
                            "runner": "claude",
                            "response": "Great question! The answer is 102.",
                        },
                        {
                            "case_id": "direct-answer",
                            "trial": 1,
                            "condition": "candidate",
                            "runner": "claude",
                            "response": "102",
                        },
                    )
                )
            )
            payload = tmp_path / "verdict.json"
            payload.write_text(json.dumps({"A": self.VERDICT, "B": self.VERDICT}))
            captured = tmp_path / "prompt.txt"
            runner_config = tmp_path / "runners.json"
            runner_config.write_text(
                json.dumps(
                    {
                        "stub": {
                            # Reads the prompt from stdin, not argv: a trailing
                            # option such as `--tools ""` otherwise swallows a
                            # prompt appended to the command line.
                            "command": ["sh", "-c", f"cat > {captured}; cat {payload}"],
                            "response_format": "text",
                        }
                    }
                )
            )
            output = tmp_path / "scores.jsonl"

            exit_code = judge.main(
                [
                    "--responses", str(responses),
                    "--cases", str(ROOT / "evals" / "cases.jsonl"),
                    "--rubric", str(ROOT / "evals" / "rubric.md"),
                    "--runner-config", str(runner_config),
                    "--runner", "stub",
                    "--output", str(output),
                ]
            )

            self.assertEqual(0, exit_code)
            rows = run_evals.read_jsonl(output)
            self.assertEqual({"baseline", "candidate"}, {row["condition"] for row in rows})

            # The scorer is the real consumer: it must accept what the judge writes.
            summary = run_evals.summarize_scores(rows)
            self.assertEqual(2, summary["conditions"]["baseline"]["rows"] + summary["conditions"]["candidate"]["rows"])

            # The prompt actually sent must carry the responses but never the conditions.
            prompt = captured.read_text()
            self.assertIn("Great question! The answer is 102.", prompt)
            self.assertNotIn("baseline", prompt.lower())
            self.assertNotIn("candidate", prompt.lower())

    def test_a_malformed_verdict_skips_its_group_instead_of_killing_the_run(self):
        # One bad grader response must not discard the groups already judged
        # nor the ones still queued behind it.
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            responses = tmp_path / "responses.jsonl"
            responses.write_text(
                "".join(
                    json.dumps(
                        {
                            "case_id": case_id,
                            "trial": 1,
                            "condition": condition,
                            "runner": "claude",
                            "response": f"{case_id} {condition} text",
                        }
                    )
                    + "\n"
                    for case_id in ("direct-answer", "casual-message")
                    for condition in ("baseline", "candidate")
                )
            )
            good = tmp_path / "good.json"
            good.write_text(json.dumps({"A": self.VERDICT, "B": self.VERDICT}))
            runner_config = tmp_path / "runners.json"
            runner_config.write_text(
                json.dumps(
                    {
                        "stub": {
                            "command": [
                                "sh",
                                "-c",
                                # `blocker` omitted for the casual-message group.
                                f'p=$(cat); case "$p" in *casual-message*)'
                                f' echo \'{{"A":{{"correctness":3}},"B":{{"correctness":3}}}}\';;'
                                f" *) cat {good};; esac",
                            ],
                            "response_format": "text",
                        }
                    }
                )
            )
            output = tmp_path / "scores.jsonl"

            exit_code = judge.main(
                [
                    "--responses", str(responses),
                    "--cases", str(ROOT / "evals" / "cases.jsonl"),
                    "--rubric", str(ROOT / "evals" / "rubric.md"),
                    "--runner-config", str(runner_config),
                    "--runner", "stub",
                    "--retries", "0",
                    "--output", str(output),
                ]
            )

            rows = run_evals.read_jsonl(output)
            self.assertEqual({"direct-answer"}, {row["case_id"] for row in rows})
            self.assertEqual(2, len(rows))
            self.assertNotEqual(0, exit_code, "skipped groups must not report success")

    def test_missing_entire_condition_fails_before_judging(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            responses = tmp_path / "responses.jsonl"
            responses.write_text(
                json.dumps(
                    {
                        "case_id": "direct-answer",
                        "trial": 1,
                        "condition": "baseline",
                        "runner": "stub",
                        "response": "102",
                    }
                )
                + "\n"
            )
            output = tmp_path / "scores.jsonl"
            runner_config = tmp_path / "runners.json"
            runner_config.write_text(
                json.dumps(
                    {
                        "stub": {
                            "command": ["sh", "-c", "exit 99"],
                            "response_format": "text",
                        }
                    }
                )
            )

            with self.assertRaisesRegex(ValueError, "missing required condition"):
                judge.main(
                    [
                        "--responses", str(responses),
                        "--runner-config", str(runner_config),
                        "--runner", "stub",
                        "--output", str(output),
                    ]
                )
            self.assertFalse(output.exists())

    def test_runner_failure_skips_its_group_and_continues(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            responses = tmp_path / "responses.jsonl"
            responses.write_text(
                "".join(
                    json.dumps(
                        {
                            "case_id": case_id,
                            "trial": 1,
                            "condition": condition,
                            "runner": "stub",
                            "response": f"{case_id} {condition} text",
                        }
                    )
                    + "\n"
                    for case_id in ("direct-answer", "casual-message")
                    for condition in ("baseline", "candidate")
                )
            )
            verdict = tmp_path / "verdict.json"
            verdict.write_text(json.dumps({"A": self.VERDICT, "B": self.VERDICT}))
            runner_config = tmp_path / "runners.json"
            runner_config.write_text(
                json.dumps(
                    {
                        "stub": {
                            "command": [
                                "sh",
                                "-c",
                                f'p=$(cat); case "$p" in *direct-answer*) exit 7;; *) cat {verdict};; esac',
                            ],
                            "response_format": "text",
                        }
                    }
                )
            )
            output = tmp_path / "scores.jsonl"

            exit_code = judge.main(
                [
                    "--responses", str(responses),
                    "--runner-config", str(runner_config),
                    "--runner", "stub",
                    "--retries", "0",
                    "--output", str(output),
                ]
            )

            rows = run_evals.read_jsonl(output)
            self.assertEqual({"casual-message"}, {row["case_id"] for row in rows})
            self.assertEqual(2, len(rows))
            self.assertNotEqual(0, exit_code, "skipped groups must not report success")


class JudgeCostAndBudgetTest(unittest.TestCase):
    """The judge reports what it actually spent and can be capped (#91)."""

    # A runner that bills $0.01 per invocation, reports that cost even when the
    # attempt fails the way a real provider does, and can be made to fail its
    # first N attempts so the retry path is exercised.
    RUNNER = (
        "sh",
        "-c",
        """
n=$(cat "$CALLS_FILE" 2>/dev/null || echo 0)
n=$((n+1))
echo "$n" > "$CALLS_FILE"
cat > /dev/null
if [ "$n" -le "$FAIL_FIRST" ]; then
  printf '{"result":"not a verdict","total_cost_usd":0.01}'
  exit 1
fi
printf '{"result":%s,"total_cost_usd":0.01}' "$VERDICT_JSON"
""",
    )

    # Case ids must exist in evals/cases.jsonl; an unknown id is a hard error.
    CASES = ("direct-answer", "casual-message", "code-answer")
    VERDICT_JSON = json.dumps(
        json.dumps(
            {
                label: {
                    "correctness": 4,
                    "autonomy": 4,
                    "actionability": 4,
                    "safety": 5,
                    "concision": 4,
                    "blocker": False,
                    "notes": "fixture",
                }
                for label in ("A", "B")
            }
        )
    )

    def _run(self, tmp_path: Path, *, groups: int, fail_first: int, budget: float, tag: str):
        import os

        responses = tmp_path / "responses.jsonl"
        responses.write_text(
            "".join(
                json.dumps(
                    {
                        "case_id": case_id,
                        "trial": 1,
                        "condition": condition,
                        "runner": "stub",
                        "response": f"{case_id} {condition} text",
                    }
                )
                + "\n"
                for case_id in self.CASES[:groups]
                for condition in ("baseline", "candidate")
            )
        )
        runner_config = tmp_path / "runners.json"
        runner_config.write_text(
            json.dumps(
                {
                    "stub": {
                        "command": list(self.RUNNER),
                        "response_format": "claude-json",
                    }
                }
            )
        )
        output = tmp_path / f"scores-{tag}.jsonl"
        calls_file = tmp_path / f"calls-{tag}"
        old = dict(os.environ)
        os.environ["CALLS_FILE"] = str(calls_file)
        os.environ["FAIL_FIRST"] = str(fail_first)
        os.environ["VERDICT_JSON"] = self.VERDICT_JSON
        try:
            import contextlib, io

            stdout, stderr = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                exit_code = judge.main(
                    [
                        "--responses", str(responses),
                        "--cases", str(ROOT / "evals" / "cases.jsonl"),
                        "--rubric", str(ROOT / "evals" / "rubric.md"),
                        "--runner-config", str(runner_config),
                        "--runner", "stub",
                        "--output", str(output),
                        "--budget-usd", str(budget),
                    ]
                )
        finally:
            os.environ.clear()
            os.environ.update(old)
        calls = int(calls_file.read_text()) if calls_file.exists() else 0
        return exit_code, calls, stdout.getvalue() + stderr.getvalue(), output

    def test_a_retried_attempt_is_counted_in_the_reported_cost(self):
        # A failed attempt is billed. With the old accounting the second group
        # reported one call's cost ($0.01) while two calls were paid for; the
        # retry here makes the gap two calls wide on purpose.
        with tempfile.TemporaryDirectory() as tmp:
            exit_code, calls, report, _ = self._run(
                Path(tmp), groups=2, fail_first=1, budget=25.0, tag="retry"
            )

            self.assertEqual(0, exit_code)
            # group 1: attempt 1 billed + fails, attempt 2 succeeds = 2 calls
            # group 2: attempt 1 succeeds = 3 calls total = $0.03
            self.assertEqual(3, calls)
            self.assertIn("Reported judge cost: $0.0300", report)
            self.assertIn("across 3 invocation(s)", report)

    def test_cost_report_matches_invocations_when_nothing_is_retried(self):
        with tempfile.TemporaryDirectory() as tmp:
            exit_code, calls, report, _ = self._run(
                Path(tmp), groups=2, fail_first=0, budget=25.0, tag="clean"
            )

            self.assertEqual(0, exit_code)
            self.assertEqual(2, calls)
            self.assertIn("Reported judge cost: $0.0200", report)

    def test_a_budget_too_small_to_cover_the_run_stops_it(self):
        # Two groups at $0.01 each need $0.03; a $0.02 ceiling must halt the run
        # instead of judging everything and only afterwards revealing the spend.
        with tempfile.TemporaryDirectory() as tmp:
            exit_code, calls, report, output = self._run(
                Path(tmp), groups=3, fail_first=0, budget=0.02, tag="budget"
            )

            self.assertEqual(2, exit_code)
            self.assertIn("exhausted", report)
            # Regression guard for the handler ordering: the generic retry
            # handler must not swallow the budget stop and continue the run.
            self.assertLess(calls, 3, "the run judged all three groups despite the ceiling")
            # The check runs before each call, so the run stops as soon as the
            # ledger covers the ceiling, overshooting by at most the one call
            # already in flight.
            self.assertLessEqual(calls, 3)
            self.assertTrue(
                str(output) in report or "Reported judge cost" in report,
                "the run must still say what it spent when it stops",
            )

    def test_budget_rejects_a_nonsensical_ceiling(self):
        for bad in ("0", "-1", "26"):
            with self.subTest(budget=bad):
                with tempfile.TemporaryDirectory() as tmp:
                    with self.assertRaisesRegex(ValueError, "budget-usd"):
                        self._run(
                            Path(tmp), groups=1, fail_first=0, budget=float(bad),
                            tag=f"bad{bad}",
                        )


if __name__ == "__main__":
    unittest.main()
