from dataclasses import dataclass

import pandas as pd

from analysis import (
    add_average_column,
    pass_rate,
    rank_students,
    study_hours_correlation,
    subject_averages,
)


@dataclass(frozen=True)
class DashboardSummary:
    student_count: int
    overall_average: float
    pass_rate: float
    top_student_name: str
    top_student_average: float
    correlation: float


def build_summary(frame: pd.DataFrame) -> DashboardSummary:
    """Build the headline metrics displayed by the web dashboard."""
    if frame.empty:
        raise ValueError("Cannot build dashboard metrics without students.")

    ranked = rank_students(frame)
    top_student = ranked.iloc[0]

    return DashboardSummary(
        student_count=len(frame),
        overall_average=float(ranked["average"].mean()),
        pass_rate=pass_rate(frame),
        top_student_name=str(top_student["name"]),
        top_student_average=float(top_student["average"]),
        correlation=study_hours_correlation(frame),
    )


def filter_ranking(frame: pd.DataFrame, minimum_average: float = 0.0) -> pd.DataFrame:
    """Return the ranking filtered by a minimum overall average."""
    if not 0 <= minimum_average <= 100:
        raise ValueError("Minimum average must be between 0 and 100.")

    ranked = rank_students(frame)
    return ranked.loc[ranked["average"] >= minimum_average].reset_index(drop=True)


def subject_chart_data(frame: pd.DataFrame) -> pd.DataFrame:
    """Return subject averages in a chart-friendly dataframe."""
    averages = subject_averages(frame)
    result = averages.rename("average").rename_axis("subject").reset_index()
    result["subject"] = result["subject"].str.replace("_", " ").str.title()
    return result


def scatter_chart_data(frame: pd.DataFrame) -> pd.DataFrame:
    """Return study-hours and average data for the dashboard scatter plot."""
    analyzed = add_average_column(frame)
    return analyzed.loc[:, ["name", "study_hours", "average"]].copy()
