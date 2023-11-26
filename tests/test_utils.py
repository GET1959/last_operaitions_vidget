import pytest
import requests

from src.utils import get_operations, get_rub_sum, table_to_dict_list


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


@pytest.mark.parametrize(
    "file_name, expected",
    [
        (
            "test.csv",
            [
                {
                    "id": 1,
                    "state": "EXECUTED",
                    "date": "2023-09-05",
                    "operationAmount": {
                        "amount": 50000,
                        "currency": {"name": "rub", "code": "RUB"},
                    },
                    "from": "user1",
                    "to": "user2",
                    "description": "перевод",
                },
                {
                    "id": 2,
                    "state": "EXECUTED",
                    "date": "2023-11-03",
                    "operationAmount": {
                        "amount": 70000,
                        "currency": {"name": "usd", "code": "USD"},
                    },
                    "from": "user2",
                    "to": "user3",
                    "description": "кредит",
                },
                {
                    "id": 3,
                    "state": "CANCELED",
                    "date": "2023-11-10",
                    "operationAmount": {
                        "amount": 20000,
                        "currency": {"name": "eur", "code": "EUR"},
                    },
                    "from": "user4",
                    "to": "user5",
                    "description": "операция не подтверждена",
                },
            ],
        ),
        (
            "test.xlsx",
            [
                {
                    "id": 1,
                    "state": "EXECUTED",
                    "date": "2023-10-01",
                    "operationAmount": {
                        "amount": 40000,
                        "currency": {"name": "rub", "code": "RUB"},
                    },
                    "from": "user0",
                    "to": "user1",
                    "description": "перевод",
                },
                {
                    "id": 2,
                    "state": "CANCELED",
                    "date": "2023-09-05",
                    "operationAmount": {
                        "amount": 20000,
                        "currency": {"name": "aud", "code": "AUD"},
                    },
                    "from": "user5",
                    "to": "user2",
                    "description": "операция не подтверждена",
                },
                {
                    "id": 3,
                    "state": "EXECUTED",
                    "date": "2023-11-07",
                    "operationAmount": {
                        "amount": 80000,
                        "currency": {"name": "usd", "code": "USD"},
                    },
                    "from": "user7",
                    "to": "user3",
                    "description": "погашение",
                },
            ],
        ),
        ("trans_3.json", None),
    ],
)
def test_table_to_dict_list(file_name, expected):
    assert table_to_dict_list(file_name) == expected
