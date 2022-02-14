import logging.config
import pickle
from typing import List

import pandas as pd
from rich.logging import RichHandler
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import LabelEncoder

from config import config

# logger
logging.config.dictConfig(config.logging_config)
logger = logging.getLogger("root")
logger.handlers[0] = RichHandler(markup=True)


def train_preprocessors_and_featurize_train_adult_dataset() -> None:
    # silver paths
    train_silver_path = "data/silver/adult.data.parquet"

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
    df_train = pd.read_parquet(train_silver_path)
    X_train, y_train = df_train[feature_names], df_train[target_name]

    # preprocessor
    ## target
    target_preprocessor = LabelEncoder()
    y_train_preproc = target_preprocessor.fit_transform(y_train)
    ## features
    feature_preprocessor = FeaturePreprocessor(
        feature_names, categorical_features, numerical_features
    )
    X_train_preproc = feature_preprocessor.fit_transform(X_train)
    logger.info("✅ feature and target preprocessors trained!")

    # store preprocessor
    pickle.dump(target_preprocessor, open("models/target-preprocessor", "wb"))
    pickle.dump(feature_preprocessor, open("models/feature-preprocessor", "wb"))
    logger.info("✅ feature and target preprocessors stored!")

    # featurize adult dataset
    df_train.loc[:, feature_names] = X_train_preproc
    df_train.loc[:, target_name] = y_train_preproc

    # gold path
    train_gold_path = "data/gold/adult.data.parquet"

    # save dataset
    df_train.to_parquet(train_gold_path)
    logger.info("✅ dataset preprocessed saved!")


class FeaturePreprocessor(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        feature_names: List[str],
        categorical_features: List[str],
        numerical_features: List[str],
    ):
        self.feature_names = feature_names
        self.categorical_features = categorical_features
        self.numerical_features = numerical_features
        self.encoders = {feature_name: None for feature_name in categorical_features}

    def fit(self, X):
        for feature_name in self.categorical_features:
            feature_name_preprocessor = LabelEncoder().fit(X[feature_name])
            self.encoders.update({feature_name: feature_name_preprocessor})
        return self

    def transform(self, X):
        X_ = X.copy()
        for feature_name in self.categorical_features:
            X_[feature_name] = self.encoders[feature_name].transform(X_[feature_name])
        return X_[self.feature_names]
