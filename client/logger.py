import logging
import sys

from sse_server.config import settings


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL)

    # Only add handler if logger doesn't already have handlers
    if not logger.handlers:
        formatter = logging.Formatter(
            "%(levelname)s:    %(asctime)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s"
        )
        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


# Create default logger
logger = get_logger(__name__)
