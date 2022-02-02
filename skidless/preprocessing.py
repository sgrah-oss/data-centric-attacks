from typing import List

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import LabelEncoder


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
