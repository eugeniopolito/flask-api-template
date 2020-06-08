"""
A simple logger decorator.

Usage:

@log()
def your_method():
    pass
"""

import functools
import logging


class log(object):
    """
    A useful logger decorator.
    """

    def __init__(self, logger=None):
        self.logger = logger

    def __call__(self, func):
        if not self.logger:
            logging.basicConfig(
                format="%(levelname)s [%(asctime)s]: %(message)s ",
                level=logging.INFO,
                datefmt="%d/%m/%Y %H:%M:%S",
            )
            self.logger = logging.getLogger(func.__module__)
            self.logger.level = logging.INFO

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self.logger.info(f"{func.__name__} {args[0]}")
            f_result = func(*args, **kwargs)
            return f_result

        return wrapper
