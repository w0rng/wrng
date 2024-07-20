import functools
import random
import time


def retry(autoretry_for=(Exception,), max_retries=3, retry_backoff=5, retry_backoff_max=100, retry_jitter=True):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except autoretry_for:
                    retries += 1
                    if retries >= max_retries:
                        raise
                    backoff_time = min(retry_backoff * (2 ** (retries - 1)), retry_backoff_max)
                    if retry_jitter:
                        backoff_time += random.uniform(0, backoff_time * 0.1)
                    time.sleep(backoff_time)

        return wrapper

    return decorator


# Пример использования:
@retry(autoretry_for=(ValueError,), max_retries=5, retry_backoff=2, retry_backoff_max=30, retry_jitter=True)
def unreliable_function():
    if random.random() > 0.01:
        print("Ошибка!")
        raise ValueError("Произошла ошибка")
    return "Успех!"


# Запуск функции для проверки
try:
    result = unreliable_function()
    print(result)
except ValueError as e:
    print(f"Не удалось выполнить функцию: {e}")
