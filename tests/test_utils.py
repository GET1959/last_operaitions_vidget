import os
import json
import pytest
import requests

from src.utils import get_operations, get_rub_sum, get_amount_in_rub, table_to_dict_list


# URL = 'https://jsonkeeper.com/b/DRYA'  # operations.json

cur_dir = os.path.dirname(os.path.abspath("."))
path_to_file = os.path.join(cur_dir + "/data/")


@pytest.fixture()
def list_of_transactions():
    with open(path_to_file + "operations.json", encoding="utf-8") as file:
        return json.load(file)


@pytest.mark.parametrize(
    "file, expected",
    [
        ("operations.json", requests.get(URL, verify=False).json()),
        (
            "list_file.json",
            [
                {"id": 441945886, "state": "EXECUTED", "date": "2019-08-26T10:50:58.294041"},
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),
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

url = "https://www.cbr-xml-daily.ru/daily_json.js"
data = requests.get(url).json()
data_dict = {currency: data["Valute"][currency]["Value"] for currency in data["Valute"]}


def test_get_amount_in_rub_usd():
    assert get_amount_in_rub("trans_2.json") == round(8221.37 * data_dict["USD"], 2)


def test_get_amount_in_rub_rub():
    assert get_amount_in_rub("trans_1.json") == 31957.58
