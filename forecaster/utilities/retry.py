import time
import logging
import asyncio
import traceback
from typing import Sequence, Type

from functools import wraps


class RetryError(Exception):
    pass


def async_retry(
    exceptions: Sequence[Type[Exception] | Type[BaseException]],
    tries: int = 0,
    delay: float = 0,
    backoff: float = 1,
    logger: logging.Logger | None = None,
):
    def wrapper(function):
        @wraps(function)
        async def inner(*args, **kwargs):
            traceback_ = ''
            _tries, _delay = tries, delay
            while _tries:
                try:
                    return await function(*args, **kwargs)
                except tuple(exceptions) as e:
                    if not traceback_:
                        traceback_ = traceback.format_exc()
                    _tries -= 1

                    if logger is not None:
                        logger.warning(
                            f"Error: '{e}' occurred during executing function: "
                            f"'{function.__qualname__}'. "
                            f"Retrying in {_delay} seconds..."
                        )
                await asyncio.sleep(_delay)
                _delay *= backoff
            raise RetryError(
                f"Retries: {tries} for "
                f"function: {function.__qualname__} ended. "
                f"{traceback_}"
            )
        return inner
    return wrapper


def retry(
    exceptions: Sequence[Type[Exception] | Type[BaseException]],
    tries: int = 0,
    delay: float = 0,
    backoff: float = 1,
):
    """
    :param exceptions: which type of exceptions should be handled for retry.
    :param tries: number of tries for function execution.
    :param delay: gap of time in seconds to wait between tries.
    :param backoff: multiplier for delay for each try.
    """
    def wrapper(function):
        @wraps(function)
        def inner(*args, **kwargs):
            traceback_ = ''
            exception = None
            _tries, _delay = tries, delay
            while _tries:
                try:
                    return function(*args, **kwargs)
                except tuple(exceptions) as e:
                    if not traceback_:
                        traceback_ = traceback.format_exc()
                    if exception is None:
                        exception = e
                    _tries -= 1

                time.sleep(_delay)
                _delay *= backoff

            if exception is not None:
                raise exception from RetryError(
                    f"Retries: {tries} for "
                    f"function: {function.__qualname__} ended. "
                    f"{traceback_}"
                )
            raise RetryError(
                f"Retries: {tries} for "
                f"function: {function.__qualname__} ended. "
                f"{traceback_}"
            )
        return inner
    return wrapper
