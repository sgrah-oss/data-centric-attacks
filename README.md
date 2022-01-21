skidless
==============================

Attack/Defence against data quality in a Machine Learning project

## Mission

For this data exploration, the Framing mandated DataStudio for:



- DATA PREPARATION - DATA QUALITY

    - Input: Extracts from different sources or sample data set

    - Output: Data quality assessment focused on relevant variables for the use case (detection of missing values, duplicates, heterogeneous formats…), data cleaning and correction, consolidated and preprocessed data set


- DATA SCIENCE - FEASIBILITY ASSESSEMENT

    - Input: Consolidated and preprocessed data set

    - Output: Quality and relevance assessment of the statistical modeling based on the sample data set, points of attention, impact analysis and precautions to take in a production/run mode


## Getting Started


Project Organization
------------
```
├── LICENSE
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── models             <- Trained models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a date (for ordering),
│                         the creator's initials, and a short `_` delimited description, e.g.
│                         `2020_06_01-initial-data-exploration`.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── src                <- Source code for use in this project.
│   ├── __init__.py    <- Makes src a Python module
│
├── config
│   ├── config.py      <- python config variables
│
├── .flake8            <- conf file of linter flake8
├── pyproject.toml     <- central configuration file for packaging and tools
├── requirements.txt   <- python dependencies
└── setup.py           <- Setup file
```

### Installation process

How to interact with the project:
```bash
make help
```

Create a Python virtual environment, install locally the package and pre-commit:
```bash
make venv
```

Update package
```bash
make update-package
```

## Clear all notebook outputs before committing

```bash
make clear-notebook-outputs
```
