import pytest

from src.decorators import log

@pytest.mark.parametrize(
    "x, y, expected",
    [
        (10, 5, 2),
        (0, 2, 0),
        (10, 0, None),
        (10, '2', None)
    ],
)
def test_decorated_function(x, y, expected):
    @log(filename="mylog.txt")
    def my_function():
        return x / y
    result = my_function()
    assert result == expected

