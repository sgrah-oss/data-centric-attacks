import threading

import typer

from skidless.cleaning import clean_adult_dataset
from skidless.datasets import download_adult_dataset
from skidless.features import train_preprocessors_and_featurize_adult_dataset
from skidless.generators import start_producing
from skidless.model import predicting_message, train_preprocessor_and_model

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
def run_train_preprocessors_and_featurize_adult_dataset():
    """Download adult dataset"""
    train_preprocessors_and_featurize_adult_dataset()


@app.command()
def run_train_preprocessor_and_model():
    """train preprocessor and model"""
    train_preprocessor_and_model()


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
