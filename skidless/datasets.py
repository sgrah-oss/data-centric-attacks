import logging.config

import pandas as pd
from rich.logging import RichHandler

from config import config

# logger
logging.config.dictConfig(config.logging_config)
logger = logging.getLogger("root")
logger.handlers[0] = RichHandler(markup=True)


def download_adult_dataset() -> None:
    train_path = config.PATH_DATA_RAW / "adult.data.csv"
    test_path = config.PATH_DATA_RAW / "adult.test.csv"

    COLUMNS = [
        "age",
        "workclass",
        "fnlwgt",
        "education",
        "education_num",
        "marital_status",
        "occupation",
        "relationship",
        "race",
        "gender",
        "capital_gain",
        "capital_loss",
        "hours_per_week",
        "native_country",
        "income_bracket",
    ]

    logger.info("downloading training data...")
    df_train = pd.read_csv(
        "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data", names=COLUMNS
    )
    df_train.drop("education_num", axis=1, inplace=True)
    df_train["income_bracket"] = (
        df_train["income_bracket"].str.strip(" ").str.replace(".", "", regex=False)
    )
    df_train.to_csv(train_path)

    logger.info("downloading testing data...")
    df_test = pd.read_csv(
        "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.test",
        names=COLUMNS,
        skiprows=1,
    )
    df_test.drop("education_num", axis=1, inplace=True)
    df_test["income_bracket"] = (
        df_test["income_bracket"].str.strip(" ").str.replace(".", "", regex=False)
    )
    df_test.to_csv(test_path)
