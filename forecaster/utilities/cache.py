import datetime
from functools import lru_cache, wraps


def timed_lru_cache(seconds: int, maxsize: int = None):
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = datetime.timedelta(seconds=seconds)
        func.expiration = datetime.datetime.now(datetime.UTC) + func.lifetime

        @wraps(func)
        async def wrapped_func(*args, **kwargs):
            if datetime.datetime.now(datetime.UTC) >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.datetime.now(datetime.UTC) + func.lifetime

            return await func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache
