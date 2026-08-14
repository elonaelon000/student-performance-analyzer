# Student Performance Analyzer

A beginner-friendly Python data analysis project that reads student performance data from a CSV file, validates the input, and produces a clear terminal report.

## Current Features

- Loads student data from CSV
- Validates required columns and input values
- Rejects missing names, invalid grades, non-numeric values, and negative study hours
- Calculates each student's average grade
- Calculates class and subject averages
- Calculates the overall pass rate
- Identifies the top-performing student
- Produces a ranked student list
- Includes automated unit tests

## Technologies

- Python
- CSV data processing
- Python standard library (`csv`, `statistics`, `pathlib`, `unittest`)
- Git and GitHub

## Project Structure

```text
dayOne/
├── app.py
├── data/
│   └── students.csv
├── tests/
│   └── test_app.py
├── .gitignore
└── README.md
```

## Run the Project

Clone the repository and enter the project folder:

```bash
git clone https://github.com/elonaelon000/dayOne.git
cd dayOne
```

Run the analyzer:

```bash
python app.py
```

## Run the Tests

The project uses Python's built-in `unittest` framework, so no external testing package is required.

```bash
python -m unittest discover -s tests -v
```

The current test suite covers:

- student average calculations
- subject average calculations
- pass-rate calculations
- valid CSV parsing
- missing CSV columns
- grades outside the 0–100 range
- non-numeric values
- negative study hours

## Example Analysis

The program reports:

- number of students analyzed
- overall class average
- pass rate
- top student
- average grade for each subject
- complete student ranking

## Data Validation

Each CSV row must contain:

```text
name,math,programming,statistics,study_hours
```

Grades must be between `0` and `100`, names cannot be empty, and study hours cannot be negative. Invalid data produces a readable error message instead of an unhandled crash.

## Why I Built This

I created this project to practice Python programming and begin applying programming concepts to data analysis. I am developing it incrementally so each version introduces a new software-engineering or data-science concept, including validation, testing, data processing, visualization, and interactive applications.

## Planned Improvements

- Pandas-based data processing
- Data visualizations with Matplotlib
- More detailed performance statistics
- Study-hours vs. performance analysis
- Interactive Streamlit dashboard
- Continuous integration with GitHub Actions

## Author

**Elona Tarja**  
Informatics Engineering Student  
Interested in Data Science, Artificial Intelligence, and Software Development
