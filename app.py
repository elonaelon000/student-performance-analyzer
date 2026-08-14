from math import isnan
from pathlib import Path

from analysis import (
    SUBJECTS,
    load_students,
    pass_rate,
    rank_students,
    study_hours_correlation,
    subject_averages,
)
from visualizations import generate_charts

DATA_FILE = Path("data/students.csv")
OUTPUT_DIR = Path("output")


def describe_correlation(value: float) -> str:
    """Return a plain-language description of a correlation value."""
    if isnan(value):
        return "not enough data"

    strength = abs(value)
    if strength >= 0.7:
        label = "strong"
    elif strength >= 0.4:
        label = "moderate"
    elif strength >= 0.2:
        label = "weak"
    else:
        label = "very weak"

    if value > 0:
        direction = "positive"
    elif value < 0:
        direction = "negative"
    else:
        direction = "no"

    return f"{label} {direction} relationship"


def print_report(students) -> None:
    """Print the pandas-based student performance report."""
    ranked = rank_students(students)
    top_student = ranked.iloc[0]
    averages = subject_averages(students)
    overall_average = float(ranked["average"].mean())
    correlation = study_hours_correlation(students)

    print("STUDENT PERFORMANCE ANALYZER - VERSION 2")
    print("-" * 42)
    print(f"Students analyzed: {len(students)}")
    print(f"Overall class average: {overall_average:.1f}%")
    print(f"Pass rate: {pass_rate(students):.1f}%")
    print()
    print("Top student:")
    print(f"{top_student['name']} - {top_student['average']:.1f}%")
    print()
    print("Subject averages:")

    for subject in SUBJECTS:
        display_name = subject.replace("_", " ").title()
        print(f"{display_name}: {averages[subject]:.1f}%")

    print()
    print("Study-hours analysis:")
    if isnan(correlation):
        print("Correlation: not enough data")
    else:
        print(f"Correlation: {correlation:.2f} ({describe_correlation(correlation)})")

    print()
    print("Student ranking:")
    for position, (_, student) in enumerate(ranked.iterrows(), start=1):
        print(f"{position}. {student['name']} - {student['average']:.1f}%")


def main() -> None:
    if not DATA_FILE.exists():
        print(f"Data file not found: {DATA_FILE}")
        return

    try:
        students = load_students(DATA_FILE)
    except (OSError, ValueError) as exc:
        print(f"Could not analyze student data: {exc}")
        return

    if students.empty:
        print("No student records were found.")
        return

    print_report(students)

    try:
        chart_paths = generate_charts(students, OUTPUT_DIR)
    except OSError as exc:
        print(f"Could not save charts: {exc}")
        return

    print()
    print("Charts created:")
    for path in chart_paths:
        print(f"- {path}")


if __name__ == "__main__":
    main()
