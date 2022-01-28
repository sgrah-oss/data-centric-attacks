import click

from skidless.datasets import download_adult_dataset
from skidless.model import train_preprocessor_and_model


@click.group()
def main():
    pass


@main.command("download-adult-dataset")
def main_download_adult_dataset():
    download_adult_dataset()


@main.command("train-preprocessor-and-model")
def main_train_preprocessor_and_model():
    train_preprocessor_and_model()


if __name__ == "__main__":
    main()
