import time

import pytest

from decorators.ratelimit import ratelimit


@pytest.fixture
def limited_function():
    @ratelimit(calls=2, period=1)
    def func():
        return "Success"

    return func


def test_ratelimit_allows_requests_within_limit(limited_function):
    assert limited_function() == "Success"
    assert limited_function() == "Success"


def test_ratelimit_exceeds_limit(limited_function):
    limited_function()
    limited_function()

    with pytest.raises(Exception, match="Rate limit exceeded"):
        limited_function()


def test_ratelimit_resets_after_period(limited_function):
    limited_function()
    limited_function()

    start_time = time.time()
    time.sleep(1.1)

    elapsed_time = time.time() - start_time
    assert elapsed_time >= 1.0

    assert limited_function() == "Success"


@pytest.mark.parametrize("calls, period", [
    (1, 1),
    (2, 1),
    (3, 1),
])
def test_ratelimit_edge_cases(calls, period):
    @ratelimit(calls=calls, period=period)
    def test_function():
        return "Success"

    for _ in range(calls):
        assert test_function() == "Success"

    time.sleep(period + 0.1)

    assert test_function() == "Success"
