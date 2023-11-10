from datetime import datetime
from functools import wraps
from typing import Callable

def log(filename: str = "mylog.txt") -> Callable:
    """
    Логирует вызов функции и ее результат в файл или в консоль. Принимает один необязательный
    аргумент filename, который определяет имя файла, в который будут записываться логи.
    Если filename не задан, то логи будут выводиться в консоль. Если вызов функции закончился ошибкой,
    то записывается сообщение об ошибке и входные параметры функции.
    :param filename:
    :return logs:
    """
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                print(f"{datetime.now().replace(microsecond=0)} {func.__name__} ok\n")
                if filename:
                    with open(filename, "a") as file:
                        file.write(f"{datetime.now().replace(microsecond=0)} {func.__name__} ok\n")
            except Exception as err:
                result = None
                print(f"{datetime.now().replace(microsecond=0)} {func.__name__} error: {err}\n")
                if filename:
                    with open(filename, "a") as file:
                        file.write(f"{datetime.now().replace(microsecond=0)} {func.__name__} error: {err}\n")
            return result
        return inner
    return wrapper
