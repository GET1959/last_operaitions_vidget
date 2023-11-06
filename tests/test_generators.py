import pytest
import requests

from src.generators import filter_by_currency, get_description, card_number_generator


# Исходный список словарей - "https://jsonkeeper.com/b/SALD"
# Фильтрованый по USD - "https://jsonkeeper.com/b/68CZ"
# Фильтрованый по RUB - "https://jsonkeeper.com/b/00FU"


@pytest.fixture()
def list_of_transactions():
    return requests.get("https://jsonkeeper.com/b/SALD", verify=False).json()


@pytest.mark.parametrize(
    "cur, expected",
    [
        ("USD", requests.get("https://jsonkeeper.com/b/68CZ", verify=False).json()),
        ("RUB", requests.get("https://jsonkeeper.com/b/00FU", verify=False).json()),
    ],
)
def test_filter_by_currency(list_of_transactions, cur, expected):
    assert list(filter_by_currency(list_of_transactions, cur)) == expected


@pytest.mark.parametrize(
    "expected",
    [
        [
            "Перевод организации",
            "Перевод со счета на счет",
            "Перевод со счета на счет",
            "Перевод с карты на карту",
            "Перевод организации",
        ]
    ],
)
def test_get_description(list_of_transactions, expected):
    assert list(get_description(list_of_transactions)) == expected


@pytest.mark.parametrize(
    "start, end, expected",
    [
        (
            1,
            5,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
                "0000 0000 0000 0004",
                "0000 0000 0000 0005",
            ],
        ),
        (
            121582,
            121589,
            [
                "0000 0000 0012 1582",
                "0000 0000 0012 1583",
                "0000 0000 0012 1584",
                "0000 0000 0012 1585",
                "0000 0000 0012 1586",
                "0000 0000 0012 1587",
                "0000 0000 0012 1588",
                "0000 0000 0012 1589",
            ],
        ),
        (
            9999999999999987,
            9999999999999995,
            [
                "9999 9999 9999 9987",
                "9999 9999 9999 9988",
                "9999 9999 9999 9989",
                "9999 9999 9999 9990",
                "9999 9999 9999 9991",
                "9999 9999 9999 9992",
                "9999 9999 9999 9993",
                "9999 9999 9999 9994",
                "9999 9999 9999 9995",
            ],
        ),
        (5, 3, []),
        (5, -5, []),
        (10000000000000000, 5, []),
    ],
)
def test_card_number_generator(start, end, expected):
    assert list(card_number_generator(start, end)) == expected


def test_card_number_generator_large_number():
    with pytest.raises(ValueError):
        list(card_number_generator(100, 10000000000000005))


def test_card_number_generator_neg_number():
    with pytest.raises(ValueError):
        list(card_number_generator(-100, 100))
