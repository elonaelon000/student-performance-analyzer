import unittest

import pandas as pd

from dashboard import (
    build_summary,
    filter_ranking,
    scatter_chart_data,
    subject_chart_data,
)


class DashboardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.students = pd.DataFrame(
            [
                {
                    "name": "Ada",
                    "math": 90.0,
                    "programming": 80.0,
                    "statistics": 70.0,
                    "study_hours": 10.0,
                },
                {
                    "name": "Ben",
                    "math": 60.0,
                    "programming": 50.0,
                    "statistics": 40.0,
                    "study_hours": 5.0,
                },
                {
                    "name": "Cara",
                    "math": 100.0,
                    "programming": 90.0,
                    "statistics": 80.0,
                    "study_hours": 15.0,
                },
            ]
        )

    def test_build_summary(self) -> None:
        summary = build_summary(self.students)
        self.assertEqual(summary.student_count, 3)
        self.assertEqual(summary.top_student_name, "Cara")
        self.assertAlmostEqual(summary.top_student_average, 90.0)
        self.assertAlmostEqual(summary.pass_rate, 200 / 3)
        self.assertGreater(summary.correlation, 0.9)

    def test_filter_ranking(self) -> None:
        filtered = filter_ranking(self.students, minimum_average=75)
        self.assertEqual(filtered["name"].tolist(), ["Cara", "Ada"])
        with self.assertRaisesRegex(ValueError, "between 0 and 100"):
            filter_ranking(self.students, minimum_average=101)

    def test_chart_data_helpers(self) -> None:
        subject_data = subject_chart_data(self.students)
        self.assertEqual(subject_data["subject"].tolist(), ["Math", "Programming", "Statistics"])
        self.assertIn("average", subject_data.columns)

        scatter_data = scatter_chart_data(self.students)
        self.assertEqual(scatter_data.columns.tolist(), ["name", "study_hours", "average"])
        self.assertEqual(len(scatter_data), 3)


if __name__ == "__main__":
    unittest.main()
