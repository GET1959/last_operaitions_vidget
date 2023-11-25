import os
import json
import pytest

from src.re_utils import table_to_dict_list, find_operation, category_count


transact_list = table_to_dict_list("transactions_excel.xlsx")


def test_find_operation():
    assert find_operation(transact_list, "Открытие") == [
        trans for trans in transact_list if "Открытие" in trans["description"]
    ]


def test_category_count():
    assert category_count(transact_list) == {
        "Перевод организации": 117,
        "Перевод с карты на карту": 587,
        "Открытие вклада": 185,
        "Перевод со счета на счет": 110,
    }
