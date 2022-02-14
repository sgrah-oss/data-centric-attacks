import logging.config
import pickle

import pandas as pd
from lightgbm import LGBMClassifier
from rich.logging import RichHandler
from sklearn.metrics import classification_report

from config import config

# logger
logging.config.dictConfig(config.logging_config)
logger = logging.getLogger("root")
logger.handlers[0] = RichHandler(markup=True)


def train_model() -> None:
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
    feature_names = numerical_features + categorical_features

    # dataset
    logger.info("getting dataset...")
    train_gold_path = "data/gold/adult.data.parquet"
    df_train = pd.read_parquet(train_gold_path)
    X_train, y_train = df_train[feature_names], df_train[target_name]
    logger.info("✅ dataset loaded!")

    # model
    logger.info("creating model...")
    model_params = {
        "learning_rate": 0.1,
        "max_depth": 3,
        "n_estimators": 300,
        "categorical_feature": [feature_names.index(col_name) for col_name in categorical_features],
        "n_jobs": 1,
        "random_state": 1234,
    }
    model = LGBMClassifier(objective="binary", **model_params).fit(X_train, y_train)
    logger.info("✅ model trained!")

    # evaluation
    logger.info("evaluating model on train dataset...")
    y_pred = model.predict(X_train)
    logger.info(classification_report(y_train, y_pred))

    # store model
    logger.info("storing model...")
    pickle.dump(model, open("models/model", "wb"))
    logger.info("✅ model stored!")
