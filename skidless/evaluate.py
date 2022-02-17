import json
import logging.config
import math
import pickle

import pandas as pd
import yaml
from rich.logging import RichHandler
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    precision_recall_curve,
    roc_auc_score,
    roc_curve,
)

from config import config

# logger
logging.config.dictConfig(config.logging_config)
logger = logging.getLogger("root")
logger.handlers[0] = RichHandler(markup=True)

# params
feature_params = yaml.safe_load(open("params.yaml"))["features"]


def evaluate_model() -> None:
    # dataset
    logger.info("getting dataset...")
    test_silver_path = "data/silver/adult.test.parquet"
    df_test = pd.read_parquet(test_silver_path)
    feature_names = feature_params["numerical_features"] + feature_params["categorical_features"]
    X_test, y_test = df_test[feature_names], df_test[feature_params["target_name"]]
    logger.info("✅ dataset loaded!")

    # preprocessors
    feature_preprocessor = pickle.load(open("models/feature-preprocessor", "rb"))
    target_preprocessor = pickle.load(open("models/target-preprocessor", "rb"))
    y_test_preproc = target_preprocessor.transform(y_test)
    X_test_preproc = feature_preprocessor.transform(X_test)
    logger.info("✅ feature and target preprocessors loaded!")

    # load model
    model = pickle.load(open("models/model", "rb"))
    predictions_by_class = model.predict_proba(X_test_preproc)
    predictions = predictions_by_class[:, 1]
    labels_predicted = model.predict(X_test_preproc)
    logger.info("✅ model predictions made!")

    # compute metrics
    accuracy = accuracy_score(y_test_preproc, labels_predicted)
    avg_prec = average_precision_score(y_test_preproc, predictions)
    roc_auc = roc_auc_score(y_test_preproc, predictions)
    precision, recall, prc_thresholds = precision_recall_curve(y_test_preproc, predictions)
    fpr, tpr, roc_thresholds = roc_curve(y_test_preproc, predictions)
    logger.info("✅ all metrics are computed!")

    # store metrics
    with open("metrics/scores.json", "w") as fd:
        json.dump({"accuracy": accuracy, "avg_prec": avg_prec, "roc_auc": roc_auc}, fd, indent=4)

    # ROC has a drop_intermediate arg that reduces the number of points.
    # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html#sklearn.metrics.roc_curve.
    # PRC lacks this arg, so we manually reduce to 1000 points as a rough estimate.
    nth_point = math.ceil(len(prc_thresholds) / 1000)
    prc_points = list(zip(precision, recall, prc_thresholds))[::nth_point]
    with open("metrics/prc.json", "w") as fd:
        json.dump(
            {"prc": [{"precision": p, "recall": r, "threshold": t} for p, r, t in prc_points]},
            fd,
            indent=4,
        )

    with open("metrics/roc.json", "w") as fd:
        json.dump(
            {
                "roc": [
                    {"fpr": fp, "tpr": tp, "threshold": t}
                    for fp, tp, t in zip(fpr, tpr, roc_thresholds)
                ]
            },
            fd,
            indent=4,
        )

    logger.info("✅ all metrics are stored!")
