import json
import os
from typing import Any

import requests


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
            return json.load(file) + []
    except json.decoder.JSONDecodeError:
        return []
    except TypeError:
        return []
    except FileNotFoundError:
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
        return float(transaction["operationAmount"]["amount"])
    raise ValueError("Транзация выполнена не в рублях. Укажите транзакцию в рублях")


def get_amount_in_rub(transaction: dict) -> Any:
    """
    Функция принимает на вход одну транзакцию
    и возвращает сумму транзакции (amount) в рублях, тип float
    :param transaction:
    :return sum of transaction:
    """
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        data_dict = {currency: data["Valute"][currency]["Value"] for currency in data["Valute"]}
        cur = transaction["operationAmount"]["currency"]["code"]
        amount = transaction["operationAmount"]["amount"]
        if cur == "RUB":
            return float(amount)
        else:
            return round(float(amount) * data_dict[cur], 2)
    else:
        return None
