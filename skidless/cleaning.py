import logging.config

import pandas as pd
import yaml
from rich.logging import RichHandler

from config import config

# logger
logging.config.dictConfig(config.logging_config)
logger = logging.getLogger("root")
logger.handlers[0] = RichHandler(markup=True)

# params
clean_params = yaml.safe_load(open("params.yaml"))["clean"]
feature_params = yaml.safe_load(open("params.yaml"))["features"]


def clean_adult_dataset() -> None:
    # bronze paths
    train_bronze_path = "data/bronze/adult.data.csv"
    test_bronze_path = "data/bronze/adult.test.csv"

    # cleaning
    df_train = pd.read_csv(train_bronze_path, names=clean_params["raw_columns"])
    df_train.drop("education_num", axis=1, inplace=True)
    df_train["income_bracket"] = (
        df_train["income_bracket"].str.strip(" ").str.replace(".", "", regex=False)
    )

    df_test = pd.read_csv(test_bronze_path, names=clean_params["raw_columns"], skiprows=1)
    df_test.drop("education_num", axis=1, inplace=True)
    df_test["income_bracket"] = (
        df_test["income_bracket"].str.strip(" ").str.replace(".", "", regex=False)
    )

    # feature types
    for column in feature_params["categorical_features"] + [feature_params["target_name"]]:
        df_train[column] = df_train[column].astype("category")
        df_test[column] = df_test[column].astype("category")
    for column in feature_params["numerical_features"]:
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
