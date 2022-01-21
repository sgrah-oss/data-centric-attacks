# setup.py
# Setup installation for the application

from pathlib import Path

from setuptools import find_namespace_packages, setup

BASE_DIR = Path(__file__).parent

# Load packages from requirements.txt
with open(Path(BASE_DIR, "requirements.txt")) as file:
    required_packages = [ln.strip() for ln in file.readlines()]

test_packages = [
    "pytest==6.0.2",
    "pytest-cov==2.10.1",
]

dev_packages = [
    "black==20.8b1",
    "flake8==3.8.3",
    "isort==5.5.3",
    "jupyterlab==3.2.0",
    "pre-commit==2.11.1",
    "vulture==2.3.0",
    "mypy==0.910",
]


setup(
    name='skidless',
    version="0.1",
    description="Attack/Defence against data quality in a Machine Learning project",
    author="kaboudan",
    license="TOTALENERGIES - TDF",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    packages=find_namespace_packages(),
    install_requires=[required_packages],
    extras_require={"test": test_packages, "dev": test_packages + dev_packages},
)
