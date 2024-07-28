from enum import StrEnum
from functools import wraps
from typing import TYPE_CHECKING, Any, Optional


if TYPE_CHECKING:
    from logging import Logger


class ModeType(StrEnum):
    PROD = 'prod'
    FAKE = 'fake'
    FAIL = 'fail'


def return_stub(stub: Any, logger: Optional['Logger'] = None, mode: ModeType = ModeType.PROD):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            def result_stub():
                return stub() if callable(stub) else stub

            if mode == ModeType.FAKE:
                if logger:
                    logger.info('Function %s not call, return stub', func)
                return result_stub()

            try:
                return func(*args, **kwargs)
            except Exception:
                if mode == ModeType.FAIL:
                    if logger:
                        logger.exception('Function %s raise Exception, return stub', func)
                    return result_stub()

                raise

        return wrapper

    return decorator


__all__ = ['return_stub', 'ModeType']
