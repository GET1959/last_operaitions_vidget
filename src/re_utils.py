import logging
import re
from collections import Counter


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


def category_count(transactions_list: list[dict]) -> dict:
    """
    Функция принимает список словарей с данными о банковских операциях и словарь категорий операций
    и возвращает словарь, в котором ключи — это названия категорий,
    а значения — это количество операций в каждой категории.
    :param transactions_list:
    :return category_count_dict:
    """
    category_count_dict = dict(
        Counter([transaction["description"] for transaction in transactions_list])
    )
    logger.info("Из списка трансакций получена статистика по категориям.")
    return category_count_dict
