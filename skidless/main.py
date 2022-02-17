import threading

import typer

from skidless.cleaning import clean_adult_dataset
from skidless.datasets import download_adult_dataset
from skidless.evaluate import evaluate_model
from skidless.features import (
    train_preprocessors_and_featurize_train_adult_dataset,
)
from skidless.generators import start_producing
from skidless.model import train_model
from skidless.predictions import predicting_message

app = typer.Typer()


@app.command()
def run_download_adult_dataset():
    """Download adult dataset"""
    download_adult_dataset()


@app.command()
def run_clean_adult_dataset():
    """Download adult dataset"""
    clean_adult_dataset()


@app.command()
def run_train_preprocessors_and_featurize_train_adult_dataset():
    """Download adult dataset"""
    train_preprocessors_and_featurize_train_adult_dataset()


@app.command()
def run_train_model():
    """train preprocessor and model"""
    train_model()


@app.command()
def run_evaluate_model():
    """evaluate model"""
    evaluate_model()


@app.command()
def run_start_producing_messages():
    """Start producing messages"""
    start_producing()
    t = threading.Thread(target=start_producing)
    t.start()


@app.command()
def run_start_predicting_messages():
    """Start predicting messages"""
    predicting_message()
