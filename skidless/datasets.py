import pandas as pd

from config import config


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

    print("downloading training data...")
    df_train = pd.read_csv(
        "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data", names=COLUMNS
    )
    df_train.drop("education_num", axis=1, inplace=True)
    df_train.to_csv(train_path)
    # df_train.to_csv(PATH/'train/train.csv')

    print("downloading testing data...")
    df_test = pd.read_csv(
        "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.test", names=COLUMNS
    )
    df_test.drop("education_num", axis=1, inplace=True)
    df_test.to_csv(test_path)
