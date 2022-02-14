import json
import logging.config
import pickle

import pandas as pd
from kafka import KafkaConsumer
from rich.logging import RichHandler

from config import config

# logger
logging.config.dictConfig(config.logging_config)
logger = logging.getLogger("root")
logger.handlers[0] = RichHandler(markup=True)


def predicting_message():
    feature_preprocessor = pickle.load(open("models/feature-preprocessor", "rb"))
    model = pickle.load(open("models/model", "rb"))
    logger.info("✅ Feature preprocessor and model loaded")

    consumer = KafkaConsumer(bootstrap_servers=config.KAFKA_HOST)  # , auto_offset_reset='earliest')
    consumer.subscribe(["app_messages"])

    logger.info("Start consuming messages...")
    for msg in consumer:
        message = json.loads(msg.value)
        request_id = message["request_id"]
        x_input = pd.DataFrame(data=message["data"], index=[request_id])
        logger.info(f"Message ID {request_id}")
        logger.info(x_input)
        message_preprocessed = feature_preprocessor.transform(x_input)
        message_prediction = model.predict(message_preprocessed)
        logger.info(f"Prediction of earning more than 50>= : {message_prediction.squeeze()}")
