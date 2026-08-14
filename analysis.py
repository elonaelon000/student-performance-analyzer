from pathlib import Path

import pandas as pd

SUBJECTS = ("math", "programming", "statistics")
REQUIRED_COLUMNS = ("name", *SUBJECTS, "study_hours")
PASSING_GRADE = 60
MIN_GRADE = 0
MAX_GRADE = 100


def load_students(file_path: Path) -> pd.DataFrame:
    """Load and validate student data from a CSV file."""
    try:
        frame = pd.read_csv(file_path)
    except pd.errors.EmptyDataError as exc:
        raise ValueError("The CSV file is empty.") from exc

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"Missing required CSV column(s): {missing}")

    frame = frame.loc[:, REQUIRED_COLUMNS].copy()
    frame["name"] = frame["name"].fillna("").astype(str).str.strip()

    if frame["name"].eq("").any():
        row_number = int(frame.index[frame["name"].eq("")][0]) + 2
        raise ValueError(f"Row {row_number}: 'name' cannot be empty.")

    numeric_columns = [*SUBJECTS, "study_hours"]
    for column in numeric_columns:
        converted = pd.to_numeric(frame[column], errors="coerce")
        invalid_mask = converted.isna()
        if invalid_mask.any():
            row_number = int(frame.index[invalid_mask][0]) + 2
            raise ValueError(f"Row {row_number}: '{column}' must contain a number.")
        frame[column] = converted.astype(float)

    for subject in SUBJECTS:
        invalid_grade = ~frame[subject].between(MIN_GRADE, MAX_GRADE)
        if invalid_grade.any():
            row_number = int(frame.index[invalid_grade][0]) + 2
            raise ValueError(
                f"Row {row_number}: '{subject}' must be between "
                f"{MIN_GRADE} and {MAX_GRADE}."
            )

    negative_hours = frame["study_hours"] < 0
    if negative_hours.any():
        row_number = int(frame.index[negative_hours][0]) + 2
        raise ValueError(f"Row {row_number}: 'study_hours' cannot be negative.")

    return frame


def add_average_column(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of the data with an overall average column."""
    result = frame.copy()
    result["average"] = result[list(SUBJECTS)].mean(axis=1)
    return result


def subject_averages(frame: pd.DataFrame) -> pd.Series:
    """Return the class average for each subject."""
    if frame.empty:
        raise ValueError("Cannot calculate subject averages without students.")
    return frame[list(SUBJECTS)].mean()


def pass_rate(frame: pd.DataFrame) -> float:
    """Return the percentage of students with a passing overall average."""
    if frame.empty:
        return 0.0
    analyzed = add_average_column(frame)
    return float((analyzed["average"] >= PASSING_GRADE).mean() * 100)


def rank_students(frame: pd.DataFrame) -> pd.DataFrame:
    """Return students ranked from highest to lowest overall average."""
    analyzed = add_average_column(frame)
    return analyzed.sort_values("average", ascending=False).reset_index(drop=True)


def study_hours_correlation(frame: pd.DataFrame) -> float:
    """Return the Pearson correlation between study hours and overall average."""
    analyzed = add_average_column(frame)
    if len(analyzed) < 2:
        return float("nan")
    return float(analyzed["study_hours"].corr(analyzed["average"]))
