import signal
from contextlib import contextmanager

from exceptions import TimeoutException


@contextmanager
def timeout(seconds, exception=TimeoutException):
    def _handle_timeout(signum, frame):
        raise exception(f"Timeout after {seconds} seconds")

    signal.signal(signal.SIGALRM, _handle_timeout)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
