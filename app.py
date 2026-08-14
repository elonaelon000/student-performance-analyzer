import csv
from pathlib import Path
from statistics import mean

DATA_FILE = Path("data/students.csv")
SUBJECTS = ("math", "programming", "statistics")
REQUIRED_COLUMNS = ("name", *SUBJECTS, "study_hours")
PASSING_GRADE = 60
MIN_GRADE = 0
MAX_GRADE = 100


def _parse_number(value: str | None, field_name: str, row_number: int) -> float:
    """Convert a CSV value to a float and raise a clear validation error."""
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"Row {row_number}: '{field_name}' must contain a number."
        ) from exc


def load_students(file_path: Path) -> list[dict]:
    """Load and validate student records from a CSV file."""
    with file_path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        if not reader.fieldnames:
            raise ValueError("The CSV file must include a header row.")

        missing_columns = [
            column for column in REQUIRED_COLUMNS if column not in reader.fieldnames
        ]
        if missing_columns:
            missing = ", ".join(missing_columns)
            raise ValueError(f"Missing required CSV column(s): {missing}")

        students = []

        for row_number, row in enumerate(reader, start=2):
            name = (row.get("name") or "").strip()
            if not name:
                raise ValueError(f"Row {row_number}: 'name' cannot be empty.")

            student = {"name": name}

            for subject in SUBJECTS:
                grade = _parse_number(row.get(subject), subject, row_number)
                if not MIN_GRADE <= grade <= MAX_GRADE:
                    raise ValueError(
                        f"Row {row_number}: '{subject}' must be between "
                        f"{MIN_GRADE} and {MAX_GRADE}."
                    )
                student[subject] = grade

            study_hours = _parse_number(
                row.get("study_hours"), "study_hours", row_number
            )
            if study_hours < 0:
                raise ValueError(
                    f"Row {row_number}: 'study_hours' cannot be negative."
                )
            student["study_hours"] = study_hours
            students.append(student)

    return students


def student_average(student: dict) -> float:
    """Return a student's average across all subjects."""
    return mean(student[subject] for subject in SUBJECTS)


def subject_average(students: list[dict], subject: str) -> float:
    """Return the class average for one subject."""
    if subject not in SUBJECTS:
        raise ValueError(f"Unknown subject: {subject}")
    if not students:
        raise ValueError("Cannot calculate a subject average without students.")
    return mean(student[subject] for student in students)


def pass_rate(students: list[dict]) -> float:
    """Return the percentage of students whose overall average is passing."""
    if not students:
        return 0.0
    passed = sum(student_average(student) >= PASSING_GRADE for student in students)
    return passed / len(students) * 100


def print_report(students: list[dict]) -> None:
    """Print a simple performance report to the terminal."""
    ranked_students = sorted(students, key=student_average, reverse=True)
    top_student = ranked_students[0]
    overall_average = mean(student_average(student) for student in students)

    print("STUDENT PERFORMANCE ANALYZER")
    print("-" * 36)
    print(f"Students analyzed: {len(students)}")
    print(f"Overall class average: {overall_average:.1f}%")
    print(f"Pass rate: {pass_rate(students):.1f}%")
    print()
    print("Top student:")
    print(f"{top_student['name']} - {student_average(top_student):.1f}%")
    print()
    print("Subject averages:")

    for subject in SUBJECTS:
        display_name = subject.replace("_", " ").title()
        print(f"{display_name}: {subject_average(students, subject):.1f}%")

    print()
    print("Student ranking:")
    for position, student in enumerate(ranked_students, start=1):
        print(f"{position}. {student['name']} - {student_average(student):.1f}%")


def main() -> None:
    if not DATA_FILE.exists():
        print(f"Data file not found: {DATA_FILE}")
        return

    try:
        students = load_students(DATA_FILE)
    except (OSError, ValueError) as exc:
        print(f"Could not analyze student data: {exc}")
        return

    if not students:
        print("No student records were found.")
        return

    print_report(students)


if __name__ == "__main__":
    main()
