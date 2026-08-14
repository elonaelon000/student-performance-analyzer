from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from analysis import SUBJECTS, add_average_column, subject_averages


def generate_charts(frame: pd.DataFrame, output_dir: Path) -> list[Path]:
    """Generate analysis charts and return the created file paths."""
    output_dir.mkdir(parents=True, exist_ok=True)
    created_files = []

    averages = subject_averages(frame)
    subject_path = output_dir / "subject_averages.png"

    plt.figure(figsize=(8, 5))
    averages.index = [subject.replace("_", " ").title() for subject in SUBJECTS]
    averages.plot(kind="bar")
    plt.title("Average Grade by Subject")
    plt.ylabel("Average grade")
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.savefig(subject_path)
    plt.close()
    created_files.append(subject_path)

    analyzed = add_average_column(frame)
    correlation_path = output_dir / "study_hours_vs_average.png"

    plt.figure(figsize=(8, 5))
    plt.scatter(analyzed["study_hours"], analyzed["average"])
    plt.title("Study Hours vs Overall Average")
    plt.xlabel("Study hours")
    plt.ylabel("Overall average")
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.savefig(correlation_path)
    plt.close()
    created_files.append(correlation_path)

    return created_files
