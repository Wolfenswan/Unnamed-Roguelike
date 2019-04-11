import logging
import time
from functools import wraps

from config_files import cfg


def debug_timer(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if cfg.DEBUG:
            start = time.time()
            result = function(*args, **kwargs)
            end = time.time()
            logging.debug("{} ran in {}s".format(function.__name__, round(end - start, 2)))
            return result
        else:
            return function(*args, **kwargs)

    return wrapper