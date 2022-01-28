import typer

from skidless.datasets import download_adult_dataset
from skidless.model import train_preprocessor_and_model

app = typer.Typer()


@app.command()
def run_download_adult_dataset():
    """Download adult dataset"""
    download_adult_dataset()


@app.command()
def run_train_preprocessor_and_model():
    """train preprocessor and model"""
    train_preprocessor_and_model()
