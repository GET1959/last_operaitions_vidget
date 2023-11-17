import pytest
import os
import json
import requests

from src.utils import get_operations, get_rub_sum, get_amount_in_rub


@pytest.fixture()
def list_of_transactions():
    cur_dir = os.path.dirname(os.path.abspath('.'))
    path_to_file = os.path.join('C:/Users/Gennady/Skypro_learning/last_operaitions_vidget/data/operations.json')
    with open(path_to_file, encoding='utf-8') as file:
        return json.load(file)
@pytest.mark.parametrize(
    "file, expected",
    [
        ('list_file.json', requests.get('https://jsonkeeper.com/b/OE99', verify=False).json()),
        # ('list_file.json', [{'id': 441945886, 'state': 'EXECUTED', 'date': '2019-08-26T10:50:58.294041'},
        #                     {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        #                     {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]),
        ("dict_file.json", []),
        ("empty_file.json", []),
        ("some_file.json", []),
    ],
)
def test_get_operations(file, expected):
    assert get_operations(file) == expected


@pytest.mark.parametrize(
    "trans_dict, currency, expected",
    [({"id": 441945886,
    "state": "EXECUTED",
    "date": "2019-08-26T10:50:58.294041",
    "operationAmount": {
      "amount": "31957.58",
      "currency": {
        "name": "руб.",
        "code": "RUB"}},
    "description": "Перевод организации",
    "from": "Maestro 1596837868705199",
    "to": "Счет 64686473678894779589"},
        "RUB",
         31957.58),
        ({"id": 873106923,
    "state": "EXECUTED",
    "date": "2019-03-23T01:09:46.296404",
    "operationAmount": {
      "amount": "43318.34",
      "currency": {
        "name": "руб.",
        "code": "RUB"}},
    "description": "Перевод со счета на счет",
    "from": "Счет 44812258784861134719",
    "to": "Счет 74489636417521191160"},
         "RUB",
         43318.34)]
)
def test_get_rub_sum(trans_dict, currency, expected):
    assert get_rub_sum(trans_dict, currency) == expected


def test_get_rub_sum_usd(list_of_transactions):
    with pytest.raises(ValueError):
        get_rub_sum(list_of_transactions[1], "RUB")


@pytest.mark.parametrize(
    "trans_dict, expected",
    [({"id": 441945886,
    "state": "EXECUTED",
    "date": "2019-08-26T10:50:58.294041",
    "operationAmount": {
      "amount": "31957.58",
      "currency": {
        "name": "руб.",
        "code": "RUB"}},
    "description": "Перевод организации",
    "from": "Maestro 1596837868705199",
    "to": "Счет 64686473678894779589"},
         31957.58),
        ({
    "id": 142264268,
    "state": "EXECUTED",
    "date": "2019-04-04T23:20:05.206878",
    "operationAmount": {
      "amount": "79114.93",
      "currency": {
        "name": "USD",
        "code": "USD"
      }
    },
    "description": "Перевод со счета на счет",
    "from": "Счет 19708645243227258542",
    "to": "Счет 75651667383060284188"},
         7051015.29)
     ]
)
def test_get_amount_in_rub(trans_dict, expected):
    assert get_amount_in_rub(trans_dict) == expected