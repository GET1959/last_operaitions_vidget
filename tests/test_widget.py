import pytest

from src.widget import date_str_to_date, get_type_and_mask


@pytest.mark.parametrize(
    "type_and_number, expected",
    [
        ("Visa Classic 6831984547677658", "Visa Classic 6831 98** **** 7658"),
        ("Visa Classic 683198454767765", "Неверно введен номер!"),
        ("Visa Classic 68319845476776581234", "Неверно введен номер!"),
        ("Visa Classic 68319845476776ab", "Неверно введен номер!"),
        ("Card 6831984547677658", "Card 6831 98** **** 7658"),
        ("Счет 40706831984547677658", "Счет **7658"),
        ("Счет 4070683198454767765", "Неверно введен номер!"),
        ("Счет 4070683198454767", "Неверно введен номер!"),
        ("Счет 40706831984547677abc", "Неверно введен номер!"),
        ("Something 40706831984547677658", "Неверно введен номер!"),
    ],
)
def test_get_type_and_mask(type_and_number, expected):
    assert get_type_and_mask(type_and_number) == expected


@pytest.mark.parametrize(
    "str_date, expected",
    [
        ("2023-07-31T20:22:53.456123", "31.07.2023"),
        ("2023-12-31 20:22:53.45", "31.12.2023"),
    ],
)
def test_date_str_to_date(str_date, expected):
    assert date_str_to_date(str_date) == expected
