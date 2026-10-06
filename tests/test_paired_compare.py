import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import run_evals  # noqa: E402


def score_row(case_id, condition, value, trial=1, blocker=False):
    return {
        "case_id": case_id,
        "trial": trial,
        "condition": condition,
        "correctness": value,
        "autonomy": value,
        "actionability": value,
        "safety": value,
        "concision": value,
        "blocker": blocker,
        "notes": "fixture",
    }


class DescriptiveStatisticsTest(unittest.TestCase):
    def test_sample_stddev_uses_ddof_1(self):
        # For [1, 2, 3, 4]: mean 2.5, sum of squared deviations 5,
        # variance 5/3, stddev sqrt(5/3).
        self.assertAlmostEqual(
            (5 / 3) ** 0.5, run_evals._sample_stddev([1.0, 2.0, 3.0, 4.0])
        )

    def test_stddev_requires_two_values(self):
        self.assertIsNone(run_evals._sample_stddev([1.0]))
        self.assertIsNone(run_evals._sample_stddev([]))

    def test_standard_error_scales_with_sqrt_n(self):
        self.assertAlmostEqual(
            run_evals._sample_stddev([2.0, 4.0, 6.0, 8.0]) / 2,
            run_evals._standard_error([2.0, 4.0, 6.0, 8.0]),
        )

    def test_mean_ci95_is_symmetric_around_the_mean(self):
        values = [3.0, 4.0, 5.0, 6.0, 7.0]
        lower, upper = run_evals._mean_ci95(values)
        mean = sum(values) / len(values)
        self.assertAlmostEqual(mean, (lower + upper) / 2, places=4)

    def test_ci95_is_none_for_a_single_value(self):
        self.assertIsNone(run_evals._mean_ci95([3.0]))


class PairedComparisonTest(unittest.TestCase):
    def test_pairs_are_aligned_by_case_and_trial_in_any_input_order(self):
        # Candidate rows are deliberately interleaved and out of order.
        scores = [
            score_row("direct-answer", "baseline", 3),
            score_row("medical-boundary", "baseline", 2),
            score_row("medical-boundary", "candidate", 5),
            score_row("direct-answer", "candidate", 4),
            score_row("direct-answer", "baseline", 3, trial=2),
            score_row("direct-answer", "candidate", 4, trial=2),
        ]

        summary = run_evals.summarize_paired(scores)

        self.assertEqual(3, summary["pairs"])
        cases = [entry["case_id"] for entry in summary["per_case"]]
        self.assertEqual(["direct-answer", "direct-answer", "medical-boundary"], cases)
        by_case = {
            (entry["case_id"], entry["trial"]): entry for entry in summary["per_case"]
        }
        self.assertEqual(
            1, by_case[("direct-answer", 1)]["correctness"]["delta"]
        )
        self.assertEqual(
            3, by_case[("medical-boundary", 1)]["correctness"]["delta"]
        )

    def test_per_case_delta_matches_the_weighted_score_difference(self):
        scores = [
            score_row("direct-answer", "baseline", 3),
            score_row("direct-answer", "candidate", 4),
        ]

        summary = run_evals.summarize_paired(scores)
        entry = summary["per_case"][0]
        weights = run_evals.WEIGHTS
        expected = sum((4 - 3) * weight for weight in weights.values())
        self.assertAlmostEqual(expected, entry["weighted_delta"], places=4)
        for metric in weights:
            self.assertEqual(3, entry[metric]["baseline"])
            self.assertEqual(4, entry[metric]["candidate"])

    def test_dimension_stats_report_wins_ties_losses(self):
        # candidate wins case a, ties case b, loses case c.
        scores = [
            score_row("a", "baseline", 2),
            score_row("a", "candidate", 5),
            score_row("b", "baseline", 4),
            score_row("b", "candidate", 4),
            score_row("c", "baseline", 5),
            score_row("c", "candidate", 3),
        ]

        summary = run_evals.summarize_paired(scores)
        delta = summary["dimensions"]["correctness"]["delta"]

        self.assertEqual(1, delta["wins"])
        self.assertEqual(1, delta["ties"])
        self.assertEqual(1, delta["losses"])
        self.assertAlmostEqual(1 / 3, delta["mean"], places=4)

    def test_significant_flag_is_true_only_when_ci_straddles_zero(self):
        # Every candidate row is one point above its baseline row: the delta
        # is constant and positive, so its CI cannot contain zero.
        scores = []
        for case in ("a", "b", "c", "d", "e", "f"):
            scores.append(score_row(case, "baseline", 3))
            scores.append(score_row(case, "candidate", 4))

        summary = run_evals.summarize_paired(scores)
        delta = summary["dimensions"]["weighted_score"]["delta"]

        self.assertTrue(delta["significant"])
        self.assertGreater(delta["ci95"][0], 0)

    def test_significant_flag_is_false_for_noise_level_differences(self):
        # Deltas alternate +1/-1: mean zero, CI centered on zero.
        scores = []
        for index, case in enumerate(("a", "b", "c", "d", "e", "f")):
            scores.append(score_row(case, "baseline", 3))
            scores.append(score_row(case, "candidate", 3 + (1 if index % 2 == 0 else -1)))

        summary = run_evals.summarize_paired(scores)
        delta = summary["dimensions"]["weighted_score"]["delta"]

        self.assertFalse(delta["significant"])
        self.assertLessEqual(delta["ci95"][0], 0)
        self.assertGreaterEqual(delta["ci95"][1], 0)

    def test_weighted_score_dimension_reuses_weights(self):
        scores = [
            score_row("a", "baseline", 2),
            score_row("a", "candidate", 3),
            score_row("b", "baseline", 4),
            score_row("b", "candidate", 5),
        ]

        summary = run_evals.summarize_paired(scores)

        weights = run_evals.WEIGHTS
        expected_delta = sum(1.0 * weight for weight in weights.values())
        self.assertAlmostEqual(
            expected_delta,
            summary["dimensions"]["weighted_score"]["delta"]["mean"],
            places=4,
        )

    def test_unpaired_conditions_are_rejected(self):
        scores = [
            score_row("a", "baseline", 3),
            score_row("b", "baseline", 3),
            score_row("a", "candidate", 4),
        ]

        with self.assertRaisesRegex(ValueError, "not judged on the same rows"):
            run_evals.summarize_paired(scores)

    def test_missing_condition_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "baseline and candidate"):
            run_evals.summarize_paired([score_row("a", "baseline", 3)])


class CompareCliTest(unittest.TestCase):
    def test_compare_cli_prints_paired_summary(self):
        scores = [
            score_row("a", "baseline", 3),
            score_row("a", "candidate", 4),
            score_row("b", "baseline", 4),
            score_row("b", "candidate", 5),
        ]
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "scores.jsonl"
            path.write_text(
                "".join(json.dumps(row) + "\n" for row in scores), encoding="utf-8"
            )
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/run_evals.py"), "compare", str(path)],
                check=True, capture_output=True, text=True, timeout=10,
            )

        summary = json.loads(result.stdout)
        self.assertEqual(2, summary["pairs"])
        self.assertEqual({"a", "b"}, {entry["case_id"] for entry in summary["per_case"]})
        for metric in (*run_evals.WEIGHTS, "weighted_score"):
            self.assertIn(metric, summary["dimensions"])
        delta = summary["dimensions"]["weighted_score"]["delta"]
        self.assertTrue(delta["significant"])

    def test_compare_cli_rejects_unpaired_rows(self):
        scores = [
            score_row("a", "baseline", 3),
            score_row("a", "candidate", 4),
            score_row("b", "candidate", 5),
        ]
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "scores.jsonl"
            path.write_text(
                "".join(json.dumps(row) + "\n" for row in scores), encoding="utf-8"
            )
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts/run_evals.py"), "compare", str(path)],
                check=False, capture_output=True, text=True, timeout=10,
            )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("not judged on the same rows", result.stderr)


if __name__ == "__main__":
    unittest.main()
