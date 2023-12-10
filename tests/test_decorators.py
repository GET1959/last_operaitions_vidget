import os.path
from datetime import datetime

import pytest

from src.decorators import log


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10, 5, " my_function ok"),
        (0, 2, " my_function ok"),
        (10, 0, " my_function error: division by zero"),
        (10, "2", " my_function error: unsupported operand type(s) for /: 'int' and 'str'"),
    ],
)
def test_log_decorator(a, b, expected):
    filename = "mylog.txt"
    if os.path.exists(filename):
        os.remove(filename)

    @log(filename)
    def my_function(x: int, y: int) -> float:
        return x / y

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    my_function(a, b)

    with open(filename) as file:
        log_message = file.read().strip()

    expected_log = now + expected

    assert log_message == expected_log


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10, 5, " my_function ok"),
        (0, 2, " my_function ok"),
        (10, 0, " my_function error: division by zero"),
        (10, "2", " my_function error: unsupported operand type(s) for /: 'int' and 'str'"),
    ],
)
def test_log_to_console(capsys, a, b, expected):
    @log()
    def my_function(x: int, y: int) -> float:
        return x / y

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    my_function(a, b)

    expected_log = now + expected
    log_message = capsys.readouterr()

    assert log_message.out.strip() == expected_log
