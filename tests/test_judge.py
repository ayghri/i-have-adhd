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


if __name__ == "__main__":
    unittest.main()
