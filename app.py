import csv
from pathlib import Path
from statistics import mean

DATA_FILE = Path("data/students.csv")
SUBJECTS = ("math", "programming", "statistics")
PASSING_GRADE = 60


def load_students(file_path: Path) -> list[dict]:
    """Load student records from a CSV file."""
    with file_path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        students = []

        for row in reader:
            student = {
                "name": row["name"],
                "math": float(row["math"]),
                "programming": float(row["programming"]),
                "statistics": float(row["statistics"]),
                "study_hours": float(row["study_hours"]),
            }
            students.append(student)

    return students


def student_average(student: dict) -> float:
    """Return a student's average across all subjects."""
    return mean(student[subject] for subject in SUBJECTS)


def subject_average(students: list[dict], subject: str) -> float:
    """Return the class average for one subject."""
    return mean(student[subject] for student in students)


def pass_rate(students: list[dict]) -> float:
    """Return the percentage of students whose overall average is passing."""
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

    students = load_students(DATA_FILE)

    if not students:
        print("No student records were found.")
        return

    print_report(students)


if __name__ == "__main__":
    main()
