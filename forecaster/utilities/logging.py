import logging


def init_logger() -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        datefmt='%d/%m/%Y %H:%M:%S',
        format='[{levelname}] [{asctime}]  {message}',
        style='{'
    )

    logger = logging.getLogger(__name__)

    logger.addHandler(logging.StreamHandler())
    
    return logger
    

logger = init_logger()
