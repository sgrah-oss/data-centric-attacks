import logging.config
import pickle

import pandas as pd
import yaml
from lightgbm import LGBMClassifier
from rich.logging import RichHandler
from sklearn.metrics import classification_report

from config import config

# logger
logging.config.dictConfig(config.logging_config)
logger = logging.getLogger("root")
logger.handlers[0] = RichHandler(markup=True)

# params
feature_params = yaml.safe_load(open("params.yaml"))["features"]
model_params = yaml.safe_load(open("params.yaml"))["model"]


def train_model() -> None:
    # dataset
    logger.info("getting dataset...")
    train_gold_path = "data/gold/adult.data.parquet"
    df_train = pd.read_parquet(train_gold_path)
    feature_names = feature_params["numerical_features"] + feature_params["categorical_features"]
    X_train, y_train = df_train[feature_names], df_train[feature_params["target_name"]]
    logger.info("✅ dataset loaded!")

    # model
    logger.info("creating model...")
    hyper_parameters = {
        "learning_rate": model_params["learning_rate"],
        "max_depth": model_params["max_depth"],
        "n_estimators": model_params["n_estimators"],
        "categorical_feature": [
            feature_names.index(col_name) for col_name in feature_params["categorical_features"]
        ],
        "n_jobs": model_params["n_jobs"],
        "random_state": model_params["random_state"],
    }
    model = LGBMClassifier(objective="binary", **hyper_parameters).fit(X_train, y_train)
    logger.info("✅ model trained!")

    # evaluation
    logger.info("evaluating model on train dataset...")
    y_pred = model.predict(X_train)
    logger.info(classification_report(y_train, y_pred))

    # store model
    logger.info("storing model...")
    pickle.dump(model, open("models/model", "wb"))
    logger.info("✅ model stored!")
