import time
from unittest.mock import MagicMock

from decorators.timer import timer


logger = MagicMock()


@timer(logger=logger)
def sample_function(x, y):
    time.sleep(0.1)  # Имитация времени выполнения функции
    return x + y


def test_timer_decorator_logs_execution_time():
    # Запуск функции, чтобы декоратор мог сработать
    result = sample_function(3, 4)

    # Проверка результата выполнения функции
    assert result == 7

    # Проверка, что метод info был вызван один раз
    assert logger.info.call_count == 1

    # Проверка содержания сообщения в логах
    log_message = logger.info.call_args[0][0]
    assert "sample_function executed in" in log_message
    assert "seconds" in log_message

    # Проверка, что время выполнения указано в формате с двумя десятичными знаками
    import re
    match = re.search(r"sample_function executed in (\d+\.\d+) seconds", log_message)
    assert match is not None
    execution_time = float(match.group(1))
    assert 0.1 <= execution_time < 0.2  # Поскольку функция спит 0.1 секунды, время может немного отличаться
