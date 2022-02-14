import logging.config

import pandas as pd
from rich.logging import RichHandler

from config import config

# logger
logging.config.dictConfig(config.logging_config)
logger = logging.getLogger("root")
logger.handlers[0] = RichHandler(markup=True)


def clean_adult_dataset() -> None:
    # bronze paths
    train_bronze_path = "data/bronze/adult.data.csv"
    test_bronze_path = "data/bronze/adult.test.csv"

    # cleaning
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
    df_train = pd.read_csv(train_bronze_path, names=COLUMNS)
    df_train.drop("education_num", axis=1, inplace=True)
    df_train["income_bracket"] = (
        df_train["income_bracket"].str.strip(" ").str.replace(".", "", regex=False)
    )

    df_test = pd.read_csv(test_bronze_path, names=COLUMNS, skiprows=1)
    df_test.drop("education_num", axis=1, inplace=True)
    df_test["income_bracket"] = (
        df_test["income_bracket"].str.strip(" ").str.replace(".", "", regex=False)
    )

    # feature types
    target_name = "income_bracket"
    numerical_features = ["age", "fnlwgt", "capital_gain", "capital_loss", "hours_per_week"]
    categorical_features = [
        "workclass",
        "education",
        "marital_status",
        "occupation",
        "relationship",
        "race",
        "gender",
        "native_country",
    ]

    for column in categorical_features + [target_name]:
        df_train[column] = df_train[column].astype("category")
        df_test[column] = df_test[column].astype("category")
    for column in numerical_features:
        df_train[column] = df_train[column].astype("float")
        df_test[column] = df_test[column].astype("float")
    logger.info("✅ training dataset cleaned!")
    logger.info("✅ test dataset cleaned!")

    # silver paths
    train_silver_path = "data/silver/adult.data.parquet"
    test_silver_path = "data/silver/adult.test.parquet"

    # save cleaned dataset
    df_train.to_parquet(train_silver_path)
    df_test.to_parquet(test_silver_path)
    logger.info("✅ dataset saved!")
