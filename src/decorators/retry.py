import functools
import random
import time


def retry(autoretry_for: list[type[BaseException]], max_retries: int, retry_backoff: int, retry_backoff_max: int,
          retry_jitter: bool):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except tuple(autoretry_for):
                    retries += 1
                    if retries >= max_retries:
                        raise
                    backoff_time = min(retry_backoff * (2 ** (retries - 1)), retry_backoff_max)
                    if retry_jitter:
                        backoff_time += random.uniform(0, backoff_time * 0.1)
                    time.sleep(backoff_time)

        return wrapper

    return decorator
