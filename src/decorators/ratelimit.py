import time
from collections import deque
from functools import wraps


def ratelimit(calls, period):
    def decorator(func):
        call_times = deque()

        @wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()

            while call_times and current_time - call_times[0] > period:
                call_times.popleft()

            if len(call_times) < calls:
                call_times.append(current_time)
                return func(*args, **kwargs)
            else:
                wait_time = period - (current_time - call_times[0])
                raise Exception(f"Rate limit exceeded. Try again in {wait_time:.2f} seconds.")

        return wrapper

    return decorator
