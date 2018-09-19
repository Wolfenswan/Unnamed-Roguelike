import logging
import time
from functools import wraps


def debug_timer(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = function(*args, **kwargs)
        end = time.time()
        logging.debug("{} ran in {}s".format(function.__name__, round(end - start, 2)))
        return result

    return wrapper