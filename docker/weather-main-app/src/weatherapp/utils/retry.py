import time
import logging

from functools import wraps

from weatherapp.Exception.exceptions import EmptyListError

logger = logging.getLogger("WeatherApp")

def retry_on_exception(exception, max_retry=3,
                       wait_time=0.5, delay=4):
    def retry_exception(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            _retry, _delay = 0, wait_time
            while _retry < max_retry:
                try:
                    return func(*args, **kwargs)
                except exception as e:
                    _retry += 1
                    if _retry == max_retry:
                        logger.error(f"{func.__name__} failed after {_retry} attempts")
                    else:
                        logger.error(f"Retrying {func.__name__} due to {type(e)} retrying in {_delay} seconds")
                time.sleep(_delay)
                _delay *= delay
        return wrapper
    return retry_exception