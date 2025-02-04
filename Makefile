# Makefile
SHELL := /bin/bash
.SHELLFLAGS = -ec
.ONESHELL:
.SILENT:

PROJECT_NAME?=skidless
PYTHON_VERSION?=3.9

normal:=$(shell tput sgr0)
cyan:=$(shell tput setaf 6)

CONDA_ACTIVATE=source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate


.PHONY: help
help:
	echo "❓ Use \`make <target>' where <target> could be"
	grep -E '^\.PHONY: [a-zA-Z0-9_-]+ .*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = "(: |##)"}; {printf "\033[36m%-30s\033[0m %s\n", $$2, $$3}'


.PHONY: create-conda-env ## 🐍 creates development environment
create-conda-env:
	conda create -y -n venv-${PROJECT_NAME} python=${PYTHON_VERSION}
	echo -e "Use: $(cyan)conda activate venv-${PROJECT_NAME}$(normal)"


.PHONY: install-dependencies ## ⏬  installs production dependencies
install-dependencies:
	$(CONDA_ACTIVATE) venv-${PROJECT_NAME}
	conda install -y -c conda-forge lightgbm=3.3.2
	pip install --upgrade pip setuptools wheel
	pip install -e ".[dev]" --no-cache-dir
	pre-commit install
	pre-commit autoupdate


.PHONY: update-package ## 📦 updates and packages app
update-package:
	$(CONDA_ACTIVATE) venv-${PROJECT_NAME}
	pip uninstall ${PROJECT_NAME} -y
	pip install -e ".[dev]"


.PHONY: download-adult-dataset ## ⏬ download the adult dataset
download-adult-dataset:
	dvc repro download-adult-dataset


.PHONY: clean-adult-dataset ## ⏬ clean the adult dataset
clean-adult-dataset:
	dvc repro clean-adult-dataset


.PHONY: train-preprocessors-and-featurize-train-adult-dataset ## ⏬ train preprocessor and featurize train adult dataset
train-preprocessors-and-featurize-train-adult-dataset:
	dvc repro train-preprocessors-and-featurize-train-adult-dataset


.PHONY: train-model ## ⏬ train model
train-model:
	dvc repro train-model


.PHONY: evaluate-model ## ⏬ evaluate model
evaluate-model:
	dvc repro evaluate-model


.PHONY: start-producing-messages ## ⏬ start producing messages
start-producing-messages:
	skidless run-start-producing-messages


.PHONY: start-predicting-messages ## ⏬ start predicting messages
start-predicting-messages:
	skidless run-start-predicting-messages


.PHONY: code-formaters ## 🏄‍ refactors code app
code-formaters:
	black .
	isort .


.PHONY: code-linter ## ✅ run code audit tool for python
code-linter:
	pylama -i E501,W503,E226 .

# For compatibility with black
# E501: Line too long
# W503: Line break occurred before binary operator
# E226: Missing white space around arithmetic operator


.PHONY: clean ## 🧹 cleans all files in package app
clean: code-formaters code-linter
	find . -type f -name "*.DS_Store" -ls -delete
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf
	find . | grep -E ".pytest_cache" | xargs rm -rf
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf
	rm -f .coverage


.PHONY: clear-notebook-outputs ## ❇️ clear outputs of notebooks
clear-notebook-outputs:
	jupyter nbconvert --clear-output --inplace notebooks/*


.PHONY: search-security-issues-in-code ## ❇️ run security checks for vulnerabilities
search-security-issues-in-code:
	-bandit -r .


.PHONY: search-vulnerabilities-in-dependencies ## ❇️ run security checks for vulnerabilities
search-vulnerabilities-in-dependencies:
	-safety check
