import time

import pytest

from exceptions import TimeoutException
from decorators.timeout import timeout


@pytest.mark.parametrize("seconds", [0.01, 0.1, 1])
def test_timeout_decorator(seconds):
    @timeout(seconds=seconds)
    def test_function():
        time.sleep(seconds + 0.01)
        return "hello"

    with pytest.raises(TimeoutException):
        test_function()


def test_timeout_decorator_with_custom_exception():
    class MyCustomException(Exception):
        pass

    @timeout(seconds=0.01, exception=MyCustomException)
    def test_function():
        time.sleep(0.02)
        return "hello"

    with pytest.raises(MyCustomException):
        test_function()
