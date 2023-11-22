import os
import json
import pytest
import requests


from src.utils import get_operations, get_rub_sum, get_amount_in_rub


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


url = "https://www.cbr-xml-daily.ru/daily_json.js"
data = requests.get(url).json()
data_dict = {currency: data["Valute"][currency]["Value"] for currency in data["Valute"]}


def test_get_amount_in_rub_usd():
    assert get_amount_in_rub("trans_2.json") == round(8221.37 * data_dict["USD"], 2)


def test_get_amount_in_rub_rub():
    assert get_amount_in_rub("trans_1.json") == 31957.58
