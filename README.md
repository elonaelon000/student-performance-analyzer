<div align="center">

# Student Performance Analyzer

**A Python data analysis project exploring academic performance, study habits, and grade correlations.**

`Python` · `pandas` · `Matplotlib` · `unittest`

</div>

---

## ✦ Overview

Student Performance Analyzer turns student CSV data into clear academic insights. It analyzes grades, compares subject performance, ranks students, examines the relationship between study hours and grades, and automatically generates visualizations.

I built this project incrementally to strengthen my skills in **Python, data analysis, statistics, testing, and modular software design**.

## ✦ What It Does

- Calculates individual and class averages
- Compares average performance across subjects
- Calculates pass rate and student rankings
- Measures **Pearson correlation** between study hours and overall grades
- Generates two Matplotlib visualizations automatically
- Validates malformed or incomplete CSV data
- Includes **11 automated tests**

## ✦ Example Output

```text
STUDENT PERFORMANCE ANALYZER - VERSION 2
------------------------------------------
Students analyzed: 5
Overall class average: 77.9%
Pass rate: 100.0%

Top student:
Mark - 89.3%

Study-hours analysis:
Correlation: 0.98 (strong positive relationship)
```

> Correlation describes an association in the available data; it does not prove that additional study hours caused the grade differences.

## ✦ Project Structure

```text
student-performance-analyzer/
├── app.py
├── analysis.py
├── visualizations.py
├── requirements.txt
├── data/
│   └── students.csv
├── tests/
│   ├── test_analysis.py
│   └── test_visualizations.py
├── output/                 # generated when the program runs
├── .gitignore
└── README.md
```

## ✦ Run Locally

```bash
git clone https://github.com/elonaelon000/student-performance-analyzer.git
cd student-performance-analyzer

python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 app.py
```

## ✦ Visualizations

Running the analyzer generates:

- `subject_averages.png` — compares average grades across subjects
- `study_hours_vs_average.png` — visualizes study hours against overall grade averages

## ✦ Testing

Run the complete test suite with:

```bash
python3 -m unittest discover -s tests -v
```

The project currently includes **11 automated tests** covering data loading, validation, averages, pass rate, ranking, correlation, and chart generation.

## ✦ What I Learned

This project started as a smaller Python exercise and developed into a more structured data-analysis application. Through the process, I practiced separating analysis from visualization and command-line logic, working with pandas, interpreting statistical relationships, validating real input data, and testing program behavior.

## ✦ Next

Future improvements I would like to explore:

- Interactive Streamlit dashboard
- CSV upload through a browser interface
- Interactive filters and metrics
- Richer statistical summaries
- GitHub Actions continuous integration

---

<div align="center">

**Elona Tarja**  
Computer Engineering Student · Data Analytics · Learning Machine Learning

</div>
