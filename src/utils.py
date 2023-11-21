import json
import os
import logging
from typing import Any

import requests


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

fh = logging.FileHandler('utils.log', mode='w', encoding='utf-8')
fh.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

logger.addHandler(fh)

def get_operations(file_name: str) -> Any:
    """
     Функция принимает на вход путь до JSON-файла и возвращает список словарей
     с данными о финансовых транзакциях. Если файл пустой, содержит не список
     или не найден, функция возвращает пустой список.
    :param file_name:
    :return list of dict:
    """
    cur_dir = os.path.dirname(os.path.abspath("."))
    path_to_file = os.path.join(cur_dir + "/data/" + file_name)
    try:
        with open(path_to_file, encoding="utf-8") as file:
            result = json.load(file) + []
            logger.info("Получен файл с данными в формате list.")
            return result
    except json.decoder.JSONDecodeError:
        logger.error("Передан пустой файл.")
        return []
    except TypeError:
        logger.error("Содержимое файла не является списком.")
        return []
    except FileNotFoundError:
        logger.error("Файл не найден.")
        return []


def get_rub_sum(transaction: dict, currency: str = "RUB") -> Any:
    """
    Функция принимает на вход одну транзакцию и возвращает:
    – сумму транзакции (amount) в рублях, тип float, если транзация совершалась в рублях.
    – ошибку ValueError с сообщением "Транзация выполнена не в рублях.
    Укажите транзакцию в рублях", если транзакция была совершена в другой валюте.
    :param transaction:
    :param currency:
    :return sum of transaction:
    """
    if transaction["operationAmount"]["currency"]["code"] == currency:
        logger.info(f"Выведена транзакция, проведенная в {currency}.")
        return float(transaction["operationAmount"]["amount"])
    logger.error(f"Транзация выполнена не в {currency}")
    raise ValueError(f"Транзация выполнена не в {currency}")


def get_amount_in_rub(file_name: str) -> Any:
    """
    Функция принимает на вход одну транзакцию
    и возвращает сумму транзакции (amount) в рублях, тип float
    :param file_name:
    :return sum of transaction:
    """
    url = "https://www.cbr-xml-daily.ru/daily_json.js"

    cur_dir = os.path.dirname(os.path.abspath("."))
    path_to_file = os.path.join(cur_dir + "/data/" + file_name)

    with open(path_to_file, encoding="utf-8") as file:
        transaction = json.load(file)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        data_dict = {currency: data["Valute"][currency]["Value"] for currency in data["Valute"]}
        cur = transaction["operationAmount"]["currency"]["code"]
        amount = transaction["operationAmount"]["amount"]
        if cur == "RUB":
            logger.info("Выведена сумма транзакции, проведенной в рублях.")
            return float(amount)
        else:
            logger.info(f"Выведен рублевый эквивалент транзакции, проведенной в {cur}.")
            return round(float(amount) * data_dict[cur], 2)
    else:
        logger.error(f"Failed to receive data. Status code: {response.status_code}")
        return None


print(get_amount_in_rub("trans_2.json"))
#print(get_operations('list_file.json'))
#print(get_operations('some_file.json'))
#print(get_operations('empty_file.json'))
#assert get_amount_in_rub('trans_2.json') == 722412.6
