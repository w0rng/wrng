from logging import Logger
from unittest.mock import Mock

import pytest

from decorators import return_stub
from decorators.return_stub import ModeType


@return_stub(stub='stubbed_value', mode=ModeType.PROD)
def prod_function(should_raise=False):
    if should_raise:
        raise ValueError("This is a test exception")
    return 'original_value'


@return_stub(stub='stubbed_value', mode=ModeType.FAKE)
def fake_function():
    return 'original_value'


@return_stub(stub='stubbed_value', mode=ModeType.FAIL)
def fail_function(should_raise=False):
    if should_raise:
        raise ValueError("This is a test exception")
    return 'original_value'


def test_prod_mode():
    assert prod_function() == 'original_value'


def test_fake_mode_with_logger():
    mock_logger = Mock(spec=Logger)

    @return_stub(stub='stubbed_value', logger=mock_logger, mode=ModeType.FAKE)
    def fake_function_with_logger():
        return 'original_value'

    assert fake_function_with_logger() == 'stubbed_value'
    mock_logger.info.assert_called_with('Function %s not call, return stub', fake_function_with_logger.__wrapped__)


def test_fake_mode_without_logger():
    assert fake_function() == 'stubbed_value'


def test_fail_mode_with_exception_and_logger():
    mock_logger = Mock(spec=Logger)

    @return_stub(stub='stubbed_value', logger=mock_logger, mode=ModeType.FAIL)
    def fail_function_with_logger(should_raise=False):
        if should_raise:
            raise ValueError("This is a test exception")
        return 'original_value'

    assert fail_function_with_logger(should_raise=True) == 'stubbed_value'
    mock_logger.exception.assert_called_with('Function %s raise Exception, return stub',
                                             fail_function_with_logger.__wrapped__)


def test_fail_mode_with_exception_without_logger():
    assert fail_function(should_raise=True) == 'stubbed_value'


def test_fail_mode_without_exception():
    assert fail_function() == 'original_value'


def test_prod_mode_with_exception():
    with pytest.raises(ValueError):
        prod_function(should_raise=True)
