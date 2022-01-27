import numpy as np
import pandas as pd
import lightgbm as lgb
import pickle
import warnings
import argparse
import os
import pdb

from pathlib import Path
from utils.preprocess_data import build_train


def create_folders():
    print("creating directory structure...")
    (PATH).mkdir(exist_ok=True)
    (TRAIN_PATH).mkdir(exist_ok=True)
    (MODELS_PATH).mkdir(exist_ok=True)
    (DATAPROCESSORS_PATH).mkdir(exist_ok=True)
    (MESSAGES_PATH).mkdir(exist_ok=True)


def train_model(hyper):
    print("creating model...")
    init_dataprocessor = 'dataprocessor_0_.p'
    dtrain = pickle.load(open(DATAPROCESSORS_PATH/init_dataprocessor, 'rb'))
    if hyper == "hyperopt":
        # from train.train_hyperopt import LGBOptimizer
        from train.train_hyperopt_mlflow import LGBOptimizer
    elif hyper == "hyperparameterhunter":
        # from train.train_hyperparameterhunter import LGBOptimizer
        from train.train_hyperparameterhunter_mlfow import LGBOptimizer
    LGBOpt = LGBOptimizer(dtrain, MODELS_PATH)
    LGBOpt.optimize(maxevals=50)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("--hyper", type=str, default="hyperopt")
    args = parser.parse_args()
    create_folders()
    download_data()
    create_data_processor()
    create_model(args.hyper)