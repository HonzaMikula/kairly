import time
from datetime import timedelta
from contextlib import contextmanager
from django.conf import settings


@contextmanager
def perf_timer(summary=None, *args, **kwargs):
    if settings.ENABLE_PERFORMANCE_TIMER:
        start = counter = time.perf_counter()

        def timer(message, *args, **kwargs):
            nonlocal counter
            counter, counter_prev = time.perf_counter(), counter
            print("{}   >".format(timedelta(seconds=counter - counter_prev)),
                  message.format(*args, **kwargs))

        yield timer

        if summary and settings.ENABLE_PERFORMANCE_TIMER:
            end = time.perf_counter()
            print("{} >>>".format(timedelta(seconds=end - start)),
                  summary.format(*args, **kwargs))

    else:
        def null_timer(message, *args, **kwargs):
            pass

        yield null_timer
