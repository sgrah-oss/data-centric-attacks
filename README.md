skidless
==============================

Attack/Defence against data quality in a Machine Learning project

## Getting Started

How to interact with the project:
```bash
make help
```

Create a Python virtual environment named `venv-skidless` with `conda`,
```bash
make create-conda-env
```

Activate
```bash
conda activate venv-skidless
```
or configure the virtual environment in your favourite IDE

Install locally the package and pre-commit:
```bash
make install-dependencies
```

## Run the data pipeline

All the stages of the data pipeline are written down in `dvc.yaml` file.

                                               +------------------------+
                                               | download-adult-dataset |
                                               +------------------------+
                                                            *
                                                            *
                                                            *
                                                +---------------------+
                                                | clean-adult-dataset |
                                                +---------------------+****
                                            *****                          *******
                                        ****                                      *****
                                     ***                                               *******
     +-------------------------------------------------------+                                 ***
     | train-preprocessors-and-featurize-train-adult-dataset |                                   *
     +-------------------------------------------------------+                                   *
                       ***              ***                                                     *
                    ***                    ***                                                  *
                  **                          ***                                               *
        +-------------+                          **                                           ***
        | train-model |***                         **                                  *******
        +-------------+   ********                   **                           *****
                                  ********             *                   *******
                                          ********      **            *****
                                                  ****    *       ****
                                                   +----------------+
                                                   | evaluate-model |
                                                   +----------------+


Execute each stage of the pipeline with `dvc` or `make`. Example:
```bash
make download-adult-dataset
```
or
```bash
dvc repro download-adult-dataset
```


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
