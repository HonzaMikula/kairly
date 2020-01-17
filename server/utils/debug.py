import time
from datetime import timedelta
from contextlib import contextmanager


@contextmanager
def perf(summary=None):
    start = counter = time.perf_counter()

    def log(message):
        nonlocal counter
        counter, counter_prev = time.perf_counter(), counter
        print("{} >>> {} ".format(timedelta(seconds=counter - counter_prev), message))

    yield log

    if summary:
        end = time.perf_counter()
        print("{} >>> {} ".format(timedelta(seconds=end - start), summary))
