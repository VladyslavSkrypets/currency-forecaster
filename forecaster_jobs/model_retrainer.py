import time
import schedule

from forecaster.utilities.logging import logger
from forecaster.ml.model import (
    run_model_training,
)


RETRAINING_INTERVAL = 2


def retrain_model() -> None:
    logger.info('[ML][RETRAINER] Start model retrainer')
    schedule.every(interval=RETRAINING_INTERVAL).hours.do(run_model_training)

    schedule.run_all()
    while True:
        schedule.run_pending()
        time.sleep(1)



if __name__ == '__main__':
    try:
        retrain_model()
    except Exception:
        logger.exception('[ML][RETRAINER] Failed to start model retrainer')
