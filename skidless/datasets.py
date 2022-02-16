import logging.config

import wget
from rich.logging import RichHandler

from config import config

# logger
logging.config.dictConfig(config.logging_config)
logger = logging.getLogger("root")
logger.handlers[0] = RichHandler(markup=True)


def download_adult_dataset() -> None:
    # bronze paths
    train_bronze_path = "data/bronze/adult.data.csv"
    test_bronze_path = "data/bronze/adult.test.csv"

    # download dataset
    wget.download(
        url="https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data",
        out=train_bronze_path,
    )
    logger.info("✅ training dataset downloaded!")
    wget.download(
        url="https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.test",
        out=test_bronze_path,
    )
    logger.info("✅ test dataset downloaded!")
