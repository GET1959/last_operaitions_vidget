import logging
import re
from collections import Counter, defaultdict

from src.utils import table_to_dict_list


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

fh = logging.FileHandler("utils.log", mode="w", encoding="utf-8")
fh.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(module)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)

logger.addHandler(fh)


def find_operation(transactions_list: list[dict], string: str) -> list[dict]:
    """
    Функция принимает список словарей с данными о банковских операциях и строку поиска
    и возвращает список словарей, у которых в описании есть данная строка.
    :param transactions_list:
    :param string:
    :return list_with_string:
    """
    result_list = [
        transaction
        for transaction in transactions_list
        if re.search(string.lower(), transaction["description"].lower())
    ]
    logger.info(f"Из списка трансакций получены трансакции по запросу {string}.")
    return result_list


TRANS_LIST = table_to_dict_list("transactions_excel.xlsx")

CAT_DICT = defaultdict(int)
for transact in TRANS_LIST:
    CAT_DICT[transact["description"]] = 0
CAT_DICT = dict(CAT_DICT)


def category_count(transactions_list: list[dict], cat_dict: dict) -> dict:
    """
    Функция принимает список словарей с данными о банковских операциях и словарь категорий операций
    и возвращает словарь, в котором ключи — это названия категорий,
    а значения — это количество операций в каждой категории.
    :param transactions_list:
    :param cat_dict:
    :return category_count_dict:
    """
    cat_counted = dict(
        Counter(
            [
                transaction["description"]
                for transaction in transactions_list
                if transaction["description"] in list(CAT_DICT)
            ]
        )
    )
    category_count_dict = {}
    for k, v in cat_dict.items():
        category_count_dict[k] = cat_counted[k]

    logger.info("Из списка трансакций получена статистика по категориям.")

    return category_count_dict


print(
    category_count(
        TRANS_LIST,
        {
            "Открытие вклада": 0,
            "Перевод со счета на счет": 0,
        },
    )
)
