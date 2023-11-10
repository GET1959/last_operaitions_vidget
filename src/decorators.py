from datetime import datetime
from functools import wraps
from typing import Callable

def log(filename: str = None) -> Callable:
    """

    :param filename:
    :return:
    """
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                print(f"{datetime.now().replace(microsecond=0)} {func.__name__} ok\n")
                with open("/content/" + filename, "a") as file:
                    file.write(f"{datetime.now().replace(microsecond=0)} {func.__name__} ok\n")
            except Exception as err:
                result = None
                print(f"{datetime.now().replace(microsecond=0)} {func.__name__} error: {err}\n")
                with open("/content/" + filename, "a") as file:
                    file.write(f"{datetime.now().replace(microsecond=0)} {func.__name__} error: {err}\n")
            return result
        return inner
    return wrapper
