import json
import random
import uuid
from time import sleep

import pandas as pd
from kafka import KafkaProducer

from config import config


def start_producing():
    # init data loader
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
    test_silver_path = "data/silver/adult.test.parquet"
    df_test = pd.read_parquet(test_silver_path)
    X_test, y_test = df_test[feature_names], df_test[target_name]
    adult_data_loader = AdultDataLoader(X_test)

    producer = KafkaProducer(bootstrap_servers=config.KAFKA_HOST)
    for i in range(200):
        message_id = str(uuid.uuid4())
        message_content = next(adult_data_loader.generate_random_single_message())
        message = {"request_id": message_id, "data": json.loads(message_content.to_json())}

        producer.send("app_messages", json.dumps(message).encode("utf-8"))
        producer.flush()

        print("\033[1;31;40m -- PRODUCER: Sent message with id {}".format(message_id))
        sleep(2)


class AdultDataLoader:
    def __init__(
        self,
        dataset: pd.DataFrame,
    ) -> None:
        self.dataset_ = dataset

    def generate_random_single_message(self) -> pd.Series:
        N = len(self.dataset_)
        idx = random.randint(0, N)
        yield self.dataset_.iloc[idx]
