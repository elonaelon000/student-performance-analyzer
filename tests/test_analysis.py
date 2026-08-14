import tempfile
import unittest
from pathlib import Path

import pandas as pd

from analysis import (
    add_average_column,
    load_students,
    pass_rate,
    rank_students,
    study_hours_correlation,
    subject_averages,
)


class StudentPerformanceAnalysisTests(unittest.TestCase):
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

    def _write_csv(self, content: str) -> Path:
        temp_file = tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8", newline=""
        )
        temp_file.write(content)
        temp_file.close()
        self.addCleanup(Path(temp_file.name).unlink, missing_ok=True)
        return Path(temp_file.name)

    def test_add_average_column(self) -> None:
        analyzed = add_average_column(self.students)
        self.assertEqual(analyzed.loc[0, "average"], 80.0)
        self.assertNotIn("average", self.students.columns)

    def test_subject_averages(self) -> None:
        averages = subject_averages(self.students)
        self.assertAlmostEqual(averages["math"], 250 / 3)

    def test_pass_rate(self) -> None:
        self.assertAlmostEqual(pass_rate(self.students), 200 / 3)
        self.assertEqual(pass_rate(self.students.iloc[0:0]), 0.0)

    def test_rank_students(self) -> None:
        ranked = rank_students(self.students)
        self.assertEqual(ranked.iloc[0]["name"], "Cara")
        self.assertEqual(ranked.iloc[-1]["name"], "Ben")

    def test_study_hours_correlation_is_positive(self) -> None:
        correlation = study_hours_correlation(self.students)
        self.assertGreater(correlation, 0.9)

    def test_load_students_parses_valid_csv(self) -> None:
        path = self._write_csv(
            "name,math,programming,statistics,study_hours\n"
            "Ada,90,80,70,10\n"
        )
        students = load_students(path)
        self.assertEqual(students.loc[0, "name"], "Ada")
        self.assertEqual(students.loc[0, "programming"], 80.0)

    def test_load_students_rejects_missing_column(self) -> None:
        path = self._write_csv(
            "name,math,programming,study_hours\n"
            "Ada,90,80,10\n"
        )
        with self.assertRaisesRegex(ValueError, "Missing required CSV column"):
            load_students(path)

    def test_load_students_rejects_grade_outside_range(self) -> None:
        path = self._write_csv(
            "name,math,programming,statistics,study_hours\n"
            "Ada,120,80,70,10\n"
        )
        with self.assertRaisesRegex(ValueError, "must be between 0 and 100"):
            load_students(path)

    def test_load_students_rejects_non_numeric_values(self) -> None:
        path = self._write_csv(
            "name,math,programming,statistics,study_hours\n"
            "Ada,ninety,80,70,10\n"
        )
        with self.assertRaisesRegex(ValueError, "must contain a number"):
            load_students(path)

    def test_load_students_rejects_negative_study_hours(self) -> None:
        path = self._write_csv(
            "name,math,programming,statistics,study_hours\n"
            "Ada,90,80,70,-1\n"
        )
        with self.assertRaisesRegex(ValueError, "cannot be negative"):
            load_students(path)


if __name__ == "__main__":
    unittest.main()
