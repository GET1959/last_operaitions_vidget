from src.re_utils import category_count, find_operation
from src.utils import table_to_dict_list


TRANS_LIST = table_to_dict_list("transactions_excel.xlsx")


def test_find_operation():
    assert find_operation(TRANS_LIST, "Открытие") == [
        trans for trans in TRANS_LIST if "Открытие" in trans["description"]
    ]


CAT_DICT = {
    "Перевод организации": 0,
    "Перевод с карты на карту": 0,
    "Открытие вклада": 0,
    "Перевод со счета на счет": 0,
}


def test_category_count():
    assert category_count(TRANS_LIST, CAT_DICT) == {
        "Перевод организации": 117,
        "Перевод с карты на карту": 587,
        "Открытие вклада": 185,
        "Перевод со счета на счет": 110,
    }
    assert category_count(
        TRANS_LIST,
        {
            "Открытие вклада": 0,
            "Перевод со счета на счет": 0,
        },
    ) == {
        "Открытие вклада": 185,
        "Перевод со счета на счет": 110,
    }
