import tempfile
import unittest
from pathlib import Path

from app import load_students, pass_rate, student_average, subject_average


class StudentPerformanceAnalyzerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.students = [
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
        ]

    def _write_csv(self, content: str) -> Path:
        temp_file = tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8", newline=""
        )
        temp_file.write(content)
        temp_file.close()
        self.addCleanup(Path(temp_file.name).unlink, missing_ok=True)
        return Path(temp_file.name)

    def test_student_average(self) -> None:
        self.assertEqual(student_average(self.students[0]), 80.0)

    def test_subject_average(self) -> None:
        self.assertEqual(subject_average(self.students, "math"), 75.0)

    def test_pass_rate(self) -> None:
        self.assertEqual(pass_rate(self.students), 50.0)
        self.assertEqual(pass_rate([]), 0.0)

    def test_load_students_parses_valid_csv(self) -> None:
        path = self._write_csv(
            "name,math,programming,statistics,study_hours\n"
            "Ada,90,80,70,10\n"
        )
        students = load_students(path)
        self.assertEqual(students[0]["name"], "Ada")
        self.assertEqual(students[0]["programming"], 80.0)

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
