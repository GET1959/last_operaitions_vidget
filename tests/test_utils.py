import pytest
import requests

from src.utils import get_operations, get_rub_sum

URL = "https://jsonkeeper.com/b/DRYA"  # operations.json


@pytest.fixture()
def list_of_transactions():
    data = requests.get(URL, verify=False).json()
    return data


@pytest.mark.parametrize(
    "file, expected",
    [
        ("operations.json", requests.get(URL, verify=False).json()),
        ("dict_file.json", []),
        ("empty_file.json", []),
        ("some_file.json", []),
    ],
)
def test_get_operations(file, expected):
    assert get_operations(file) == expected


@pytest.mark.parametrize("currency, expected", [("RUB", 31957.58)])
def test_get_rub_sum(list_of_transactions, currency, expected):
    assert get_rub_sum(list_of_transactions[0], currency) == expected


def test_get_rub_sum_usd(list_of_transactions):
    with pytest.raises(ValueError):
        get_rub_sum(list_of_transactions[1], "RUB")
