# Student Performance Analyzer

A Python data-analysis project that reads student performance data from CSV, validates the dataset, calculates academic metrics with pandas, studies the relationship between study hours and grades, and generates visualizations with Matplotlib.

## Version 2 Highlights

Version 2 moves the project from basic Python data processing to a more realistic data-analysis workflow.

- Uses **pandas** for loading, validating, transforming, and analyzing data
- Calculates student averages, subject averages, pass rate, and ranking
- Calculates the **Pearson correlation** between study hours and overall grades
- Generates two **Matplotlib** charts automatically
- Keeps readable validation errors for malformed CSV data
- Includes automated tests for both analysis and visualization code
- Separates the project into analysis, visualization, and command-line layers

## Technologies

- Python
- pandas
- Matplotlib
- CSV
- unittest
- Git and GitHub

## Project Structure

```text
dayOne/
|-- app.py
|-- analysis.py
|-- visualizations.py
|-- requirements.txt
|-- data/
|   `-- students.csv
|-- tests/
|   |-- test_analysis.py
|   `-- test_visualizations.py
|-- output/                 # generated when the program runs
|-- .gitignore
`-- README.md
```

## Setup

Clone the repository and enter the project folder:

```bash
git clone https://github.com/elonaelon000/dayOne.git
cd dayOne
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
python3 -m pip install -r requirements.txt
```

## Run the Analyzer

```bash
python3 app.py
```

With the included sample dataset, the program reports results such as:

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

It also prints subject averages and a complete student ranking.

## Visualizations

Running the program creates an `output/` directory with:

```text
output/
|-- subject_averages.png
`-- study_hours_vs_average.png
```

The first chart compares average grades across subjects. The second is a scatter plot showing study hours against each student's overall average.

## Correlation Analysis

The project calculates the Pearson correlation coefficient between `study_hours` and each student's overall grade average.

A positive value means that higher study hours tend to appear alongside higher grades in the dataset. A negative value means the variables tend to move in opposite directions.

**Important:** correlation describes an association in the available data; it does not prove that additional study hours caused the grade differences.

## Data Validation

The CSV file must contain these columns:

```text
name,math,programming,statistics,study_hours
```

Validation rules include:

- names cannot be empty
- grades must be numeric
- grades must be between `0` and `100`
- study hours must be numeric
- study hours cannot be negative

Invalid input produces a readable error rather than an unhandled crash.

## Run the Tests

```bash
python3 -m unittest discover -s tests -v
```

The Version 2 suite contains **11 automated tests** covering data loading, validation, averages, pass rate, ranking, correlation, and chart generation.

## Why I Built This

I am developing this project incrementally to practice both software engineering and data-science concepts. Version 1 established validation and testing with the Python standard library. Version 2 introduces pandas, visualization, statistical analysis, dependency management, and a more modular project structure.

## Next Steps

Planned Version 3 improvements include:

- interactive Streamlit dashboard
- CSV upload through a browser interface
- interactive filters and metrics
- richer statistical summaries
- GitHub Actions continuous integration

## Author

**Elona Tarja**  
Informatics Engineering Student  
Interested in Data Science, Artificial Intelligence, and Software Development
