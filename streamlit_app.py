from math import isnan
from pathlib import Path

import streamlit as st

from analysis import describe_correlation, load_students
from dashboard import (
    build_summary,
    filter_ranking,
    scatter_chart_data,
    subject_chart_data,
)

DATA_FILE = Path("data/students.csv")

st.set_page_config(
    page_title="Student Performance Analyzer",
    page_icon="📊",
    layout="wide",
)

st.title("Student Performance Analyzer")
st.caption(
    "Version 3 · Upload a CSV or explore the sample dataset with interactive analytics."
)

st.sidebar.header("Dataset")
uploaded_file = st.sidebar.file_uploader(
    "Upload student data",
    type=["csv"],
    help="Expected columns: name, math, programming, statistics, study_hours",
)

if uploaded_file is None:
    data_source = DATA_FILE
    source_label = "Included sample dataset"
else:
    data_source = uploaded_file
    source_label = f"Uploaded file: {uploaded_file.name}"

st.sidebar.caption(source_label)
minimum_average = st.sidebar.slider(
    "Minimum average shown in ranking",
    min_value=0,
    max_value=100,
    value=0,
    step=5,
)

with st.sidebar.expander("Expected CSV format"):
    st.code(
        "name,math,programming,statistics,study_hours\n"
        "Ada,90,85,88,10\n"
        "Ben,72,78,75,7",
        language="text",
    )

try:
    students = load_students(data_source)
except (OSError, ValueError) as exc:
    st.error(f"Could not analyze this dataset: {exc}")
    st.stop()

if students.empty:
    st.warning("The dataset contains no student records.")
    st.stop()

summary = build_summary(students)

metric_columns = st.columns(5)
metric_columns[0].metric("Students", summary.student_count)
metric_columns[1].metric("Class average", f"{summary.overall_average:.1f}%")
metric_columns[2].metric("Pass rate", f"{summary.pass_rate:.1f}%")
metric_columns[3].metric(
    "Top student",
    summary.top_student_name,
    f"{summary.top_student_average:.1f}% average",
)
metric_columns[4].metric(
    "Study-hours correlation",
    "N/A" if isnan(summary.correlation) else f"{summary.correlation:.2f}",
)

st.divider()
st.subheader("Student ranking")
ranking = filter_ranking(students, minimum_average)

if ranking.empty:
    st.info("No students match the selected minimum average.")
else:
    ranking_display = ranking.loc[
        :, ["name", "math", "programming", "statistics", "study_hours", "average"]
    ].copy()
    ranking_display.index = ranking_display.index + 1
    ranking_display.index.name = "Rank"
    ranking_display = ranking_display.rename(
        columns={
            "name": "Name",
            "math": "Math",
            "programming": "Programming",
            "statistics": "Statistics",
            "study_hours": "Study hours",
            "average": "Average",
        }
    )
    ranking_display[["Math", "Programming", "Statistics", "Average"]] = (
        ranking_display[["Math", "Programming", "Statistics", "Average"]].round(1)
    )
    st.dataframe(ranking_display, width="stretch")

chart_columns = st.columns(2)

with chart_columns[0]:
    st.subheader("Average grade by subject")
    subject_data = subject_chart_data(students)
    st.bar_chart(
        subject_data,
        x="subject",
        y="average",
        x_label="Subject",
        y_label="Average grade",
        height=400,
    )

with chart_columns[1]:
    st.subheader("Study hours vs. performance")
    scatter_data = scatter_chart_data(students)
    st.scatter_chart(
        scatter_data,
        x="study_hours",
        y="average",
        x_label="Study hours",
        y_label="Overall average",
        color="name",
        height=400,
    )

st.subheader("Correlation interpretation")
if isnan(summary.correlation):
    st.info("There is not enough variation in the dataset to calculate a correlation.")
else:
    st.write(
        f"Pearson correlation: **{summary.correlation:.2f}** — "
        f"{describe_correlation(summary.correlation)}."
    )

st.caption(
    "Correlation describes association in the uploaded dataset; it does not establish causation."
)
