from functools import wraps

from context_managers.timeout import timeout as _timeout
from exceptions import TimeoutException


def timeout(seconds, exception=TimeoutException):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with _timeout(seconds, exception):
                return func(*args, **kwargs)

        return wrapper

    return decorator
