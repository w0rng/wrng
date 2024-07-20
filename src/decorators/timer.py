import time
from functools import wraps
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logging import Logger


def timer(logger: 'Logger'):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                return func(*args, **kwargs)
            finally:
                logger.info(f"{func.__name__} executed in {time.time() - start:.2f} seconds")

        return wrapper

    return decorator
