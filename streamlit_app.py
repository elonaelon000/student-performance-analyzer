from html import escape
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
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)


CUSTOM_CSS = """
<style>
:root {
    --bg: #08080c;
    --panel: #111116;
    --panel-soft: #16161d;
    --text: #f7f7fb;
    --muted: #a7a7b2;
    --pink: #ff2f86;
    --pink-soft: #ff78ae;
    --border: rgba(255, 255, 255, 0.09);
}

.stApp {
    background:
        radial-gradient(circle at 82% 3%, rgba(255, 47, 134, 0.13), transparent 26rem),
        radial-gradient(circle at 8% 28%, rgba(255, 47, 134, 0.06), transparent 22rem),
        var(--bg);
    color: var(--text);
}

[data-testid="stHeader"] {
    background: rgba(8, 8, 12, 0.92);
}

[data-testid="stSidebar"] {
    background: #0d0d12;
    border-right: 1px solid var(--border);
}

.block-container {
    max-width: 1240px;
    padding-top: 2.3rem;
    padding-bottom: 4rem;
}

.hero {
    position: relative;
    overflow: hidden;
    padding: 3rem 3.2rem;
    border: 1px solid var(--border);
    border-radius: 30px;
    background: linear-gradient(135deg, rgba(20, 20, 27, 0.98), rgba(10, 10, 14, 0.98));
    box-shadow: 0 24px 80px rgba(0, 0, 0, 0.28);
    margin-bottom: 1.5rem;
}

.hero::after {
    content: "";
    position: absolute;
    width: 23rem;
    height: 23rem;
    border-radius: 50%;
    right: -8rem;
    top: -10rem;
    background: radial-gradient(circle, rgba(255, 47, 134, 0.25), rgba(255, 47, 134, 0));
    pointer-events: none;
}

.eyebrow {
    color: var(--pink-soft);
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.hero h1 {
    color: var(--text);
    font-size: clamp(2.4rem, 6vw, 5.2rem);
    line-height: 0.95;
    letter-spacing: -0.055em;
    margin: 0 0 1.2rem 0;
    max-width: 880px;
}

.hero h1 span {
    color: var(--pink);
}

.hero p {
    color: #c6c6cf;
    font-size: 1.05rem;
    line-height: 1.72;
    max-width: 720px;
    margin: 0;
}

.hero-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.55rem;
    margin-top: 1.45rem;
}

.hero-tag,
.source-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.44rem 0.75rem;
    border-radius: 999px;
    border: 1px solid rgba(255, 47, 134, 0.28);
    background: rgba(255, 47, 134, 0.08);
    color: #ffd5e7;
    font-size: 0.78rem;
    font-weight: 700;
}

.section-kicker {
    color: var(--pink);
    font-size: 0.76rem;
    font-weight: 800;
    letter-spacing: 0.17em;
    text-transform: uppercase;
    margin-bottom: 0.35rem;
}

.section-title {
    color: var(--text);
    font-size: clamp(1.7rem, 3vw, 2.45rem);
    font-weight: 760;
    letter-spacing: -0.035em;
    margin: 0 0 0.5rem 0;
}

.section-copy {
    color: var(--muted);
    margin-bottom: 1.2rem;
}

.feature-card,
.metric-card,
.insight-card,
.empty-state {
    height: 100%;
    border: 1px solid var(--border);
    border-radius: 22px;
    background: linear-gradient(180deg, rgba(19, 19, 25, 0.94), rgba(13, 13, 18, 0.94));
    padding: 1.35rem;
}

.feature-index,
.metric-icon {
    color: var(--pink);
    font-size: 0.9rem;
    font-weight: 850;
    letter-spacing: 0.09em;
    margin-bottom: 0.75rem;
}

.feature-card h3,
.insight-card h3 {
    color: var(--text);
    font-size: 1.05rem;
    margin: 0 0 0.45rem 0;
}

.feature-card p,
.insight-card p,
.empty-state p {
    color: var(--muted);
    line-height: 1.55;
    margin: 0;
}

.metric-label {
    color: var(--muted);
    font-size: 0.8rem;
    font-weight: 700;
    margin-bottom: 0.35rem;
}

.metric-value {
    color: var(--text);
    font-size: clamp(1.35rem, 2.3vw, 2.15rem);
    font-weight: 780;
    letter-spacing: -0.035em;
    line-height: 1.1;
}

.metric-note {
    color: #8f8f9b;
    font-size: 0.75rem;
    margin-top: 0.45rem;
}

.empty-state {
    text-align: center;
    padding: 2.1rem 1.5rem;
    margin-top: 1rem;
}

.empty-state .empty-icon {
    width: 3.2rem;
    height: 3.2rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 16px;
    margin-bottom: 0.9rem;
    color: var(--pink);
    background: rgba(255, 47, 134, 0.1);
    border: 1px solid rgba(255, 47, 134, 0.2);
    font-size: 1.35rem;
}

div[data-testid="stFileUploader"] {
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 0.2rem 0.8rem 0.8rem 0.8rem;
    background: rgba(17, 17, 22, 0.72);
}

div[data-testid="stFileUploaderDropzone"] {
    border: 1px dashed rgba(255, 47, 134, 0.42);
    background: rgba(255, 47, 134, 0.035);
    border-radius: 16px;
}

.stButton > button {
    width: 100%;
    min-height: 3rem;
    border-radius: 999px;
    border: 1px solid rgba(255, 47, 134, 0.35);
    background: linear-gradient(90deg, #ff2f86, #ff5c9f);
    color: white;
    font-weight: 800;
    box-shadow: none;
}

.stButton > button:hover {
    border-color: #ff78ae;
    color: white;
    transform: translateY(-1px);
}

[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 0.45rem;
    background: rgba(17, 17, 22, 0.74);
    padding: 0.4rem;
    border: 1px solid var(--border);
    border-radius: 999px;
    width: fit-content;
}

[data-testid="stTabs"] button {
    border-radius: 999px;
    padding-left: 1rem;
    padding-right: 1rem;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 18px;
    overflow: hidden;
}

hr {
    border-color: var(--border) !important;
}

.footer-note {
    color: #777783;
    text-align: center;
    font-size: 0.78rem;
    margin-top: 2.2rem;
}

@media (max-width: 720px) {
    .block-container {
        padding-top: 1rem;
    }

    .hero {
        padding: 2rem 1.35rem;
        border-radius: 24px;
    }

    .hero h1 {
        font-size: 2.5rem;
    }
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

if "demo_mode" not in st.session_state:
    st.session_state.demo_mode = False
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

st.markdown(
    """
    <section class="hero">
        <div class="eyebrow">Academic data, reframed</div>
        <h1>Student <span>Performance</span> Analyzer</h1>
        <p>
            Turn student data into clear academic insights. Upload a CSV to explore
            performance, compare subjects, study ranking patterns, and examine how
            study time relates to results.
        </p>
        <div class="hero-tags">
            <span class="hero-tag">Python</span>
            <span class="hero-tag">pandas</span>
            <span class="hero-tag">Streamlit</span>
            <span class="hero-tag">Data analysis</span>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

upload_col, demo_col = st.columns([3.2, 1])
with upload_col:
    uploaded_file = st.file_uploader(
        "Upload student data",
        type=["csv"],
        key=f"dataset_upload_{st.session_state.uploader_key}",
        help="Required columns: name, math, programming, statistics, study_hours",
    )
with demo_col:
    st.markdown("<div style='height: 1.8rem'></div>", unsafe_allow_html=True)
    if st.button("Try demo dataset", use_container_width=True):
        st.session_state.demo_mode = True
        st.rerun()

if uploaded_file is not None:
    st.session_state.demo_mode = False
    data_source = uploaded_file
    source_label = f"Uploaded file · {uploaded_file.name}"
elif st.session_state.demo_mode:
    data_source = DATA_FILE
    source_label = "Demo dataset"
else:
    data_source = None
    source_label = ""

if data_source is None:
    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-icon">↗</div>
            <h3 style="margin:0 0 .45rem 0; color:#f7f7fb;">Your dashboard starts with your data.</h3>
            <p>
                Nothing is preloaded. Upload a CSV to begin, or use the demo dataset
                only when you want to preview the analysis experience.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height: 1.2rem'></div>", unsafe_allow_html=True)
    feature_columns = st.columns(3)
    features = [
        (
            "01",
            "Validate",
            "Catch missing columns, invalid grades, empty names, and malformed data before analysis.",
        ),
        (
            "02",
            "Understand",
            "See class performance, subject averages, pass rate, and a ranked student view at a glance.",
        ),
        (
            "03",
            "Discover patterns",
            "Explore the relationship between study time and academic performance without overstating causation.",
        ),
    ]
    for column, (index, title, copy) in zip(feature_columns, features):
        with column:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-index">{index}</div>
                    <h3>{title}</h3>
                    <p>{copy}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with st.expander("CSV format"):
        st.code(
            "name,math,programming,statistics,study_hours
"
            "Ada,90,85,88,10
"
            "Ben,72,78,75,7",
            language="text",
        )
    st.stop()

with st.sidebar:
    st.markdown("### Dataset")
    st.caption(source_label)
    minimum_average = st.slider(
        "Minimum average in ranking",
        min_value=0,
        max_value=100,
        value=0,
        step=5,
    )
    with st.expander("Expected CSV format"):
        st.code(
            "name,math,programming,statistics,study_hours
"
            "Ada,90,85,88,10
"
            "Ben,72,78,75,7",
            language="text",
        )
    if st.button("Start over", use_container_width=True):
        st.session_state.demo_mode = False
        st.session_state.uploader_key += 1
        st.rerun()

try:
    students = load_students(data_source)
except (OSError, ValueError) as exc:
    st.error(f"Could not analyze this dataset: {exc}")
    st.stop()

if students.empty:
    st.warning("The dataset contains no student records.")
    st.stop()

summary = build_summary(students)
ranking = filter_ranking(students, minimum_average)
subject_data = subject_chart_data(students)
scatter_data = scatter_chart_data(students)

correlation_value = "N/A" if isnan(summary.correlation) else f"{summary.correlation:.2f}"
correlation_note = (
    "Not enough variation"
    if isnan(summary.correlation)
    else describe_correlation(summary.correlation)
)

st.markdown(
    f'<span class="source-badge">● {escape(source_label)}</span>',
    unsafe_allow_html=True,
)
st.markdown("<div style='height: .75rem'></div>", unsafe_allow_html=True)


def metric_card(icon: str, label: str, value: str, note: str = "") -> str:
    safe_value = escape(str(value))
    safe_note = escape(str(note))
    return f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-label">{escape(label)}</div>
        <div class="metric-value">{safe_value}</div>
        <div class="metric-note">{safe_note}</div>
    </div>
    """


overview_tab, ranking_tab, insights_tab = st.tabs(["Overview", "Ranking", "Insights"])

with overview_tab:
    st.markdown('<div class="section-kicker">Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">The class, at a glance.</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-copy">A fast read of the most important signals in the loaded dataset.</div>',
        unsafe_allow_html=True,
    )

    metric_row_one = st.columns(3)
    metric_row_one[0].markdown(
        metric_card("01", "Students", summary.student_count, "records analyzed"),
        unsafe_allow_html=True,
    )
    metric_row_one[1].markdown(
        metric_card("02", "Class average", f"{summary.overall_average:.1f}%", "across all subjects"),
        unsafe_allow_html=True,
    )
    metric_row_one[2].markdown(
        metric_card("03", "Pass rate", f"{summary.pass_rate:.1f}%", "students meeting the pass threshold"),
        unsafe_allow_html=True,
    )

    metric_row_two = st.columns(2)
    metric_row_two[0].markdown(
        metric_card(
            "★",
            "Top student",
            summary.top_student_name,
            f"{summary.top_student_average:.1f}% overall average",
        ),
        unsafe_allow_html=True,
    )
    metric_row_two[1].markdown(
        metric_card("↔", "Study-performance correlation", correlation_value, correlation_note),
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
    chart_columns = st.columns(2)

    with chart_columns[0]:
        st.markdown('<div class="section-kicker">Subjects</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title" style="font-size:1.55rem;">Subject performance</div>', unsafe_allow_html=True)
        st.bar_chart(
            subject_data,
            x="subject",
            y="average",
            x_label="Subject",
            y_label="Average grade",
            height=390,
        )

    with chart_columns[1]:
        st.markdown('<div class="section-kicker">Study patterns</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title" style="font-size:1.55rem;">Study time vs. performance</div>', unsafe_allow_html=True)
        st.scatter_chart(
            scatter_data,
            x="study_hours",
            y="average",
            x_label="Study hours",
            y_label="Overall average",
            color="name",
            height=390,
        )

with ranking_tab:
    st.markdown('<div class="section-kicker">Ranking</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">See the class in order.</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-copy">Use the sidebar filter to focus on students above a selected overall average.</div>',
        unsafe_allow_html=True,
    )

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

with insights_tab:
    st.markdown('<div class="section-kicker">Insights</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">What the data suggests.</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-copy">Concise observations generated from the currently loaded dataset.</div>',
        unsafe_allow_html=True,
    )

    if subject_data.empty:
        strongest_subject = "N/A"
        strongest_average = "N/A"
    else:
        strongest_row = subject_data.loc[subject_data["average"].idxmax()]
        strongest_subject = str(strongest_row["subject"])
        strongest_average = f"{float(strongest_row['average']):.1f}%"

    if isnan(summary.correlation):
        correlation_copy = "There is not enough variation in the dataset to calculate a reliable correlation."
    else:
        correlation_copy = (
            f"Pearson correlation is {summary.correlation:.2f}, described as "
            f"{describe_correlation(summary.correlation)}. This is an association, not proof of causation."
        )

    insight_columns = st.columns(3)
    insight_columns[0].markdown(
        f"""
        <div class="insight-card">
            <div class="feature-index">TOP SUBJECT</div>
            <h3>{escape(strongest_subject)}</h3>
            <p>Highest subject average in this dataset: {escape(strongest_average)}.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    insight_columns[1].markdown(
        f"""
        <div class="insight-card">
            <div class="feature-index">TOP PERFORMER</div>
            <h3>{escape(summary.top_student_name)}</h3>
            <p>Leads the current ranking with an overall average of {summary.top_student_average:.1f}%.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    insight_columns[2].markdown(
        f"""
        <div class="insight-card">
            <div class="feature-index">STUDY PATTERN</div>
            <h3>{escape(correlation_value)}</h3>
            <p>{escape(correlation_copy)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    '<div class="footer-note">Student Performance Analyzer · Python · pandas · Streamlit</div>',
    unsafe_allow_html=True,
)
