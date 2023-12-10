import json
import logging
import os
from typing import Any

import pandas as pd
import requests


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

fh = logging.FileHandler("utils.log", mode="w", encoding="utf-8")
fh.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(module)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)

logger.addHandler(fh)


def get_operations(file: str) -> Any:
    """
     Функция принимает на вход путь до JSON-файла и возвращает список словарей
     с данными о финансовых транзакциях. Если файл пустой, содержит не список
     или не найден, функция возвращает пустой список.
    :param file:
    :return list of dict:
    """
    cur_dir = os.path.dirname(os.path.dirname(__file__))
    path_to_file = os.path.join(cur_dir + "/data/" + file)
    try:
        with open(path_to_file, encoding="utf-8") as f:
            result = json.load(f) + []
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


def get_amount_in_rub(file: str) -> Any:
    """
    Функция принимает на вход одну транзакцию
    и возвращает сумму транзакции (amount) в рублях, тип float
    :param file:
    :return sum of transaction:
    """
    url = "https://www.cbr-xml-daily.ru/daily_json.js"

    cur_dir = os.path.dirname(os.path.dirname(__file__))
    path_to_file = os.path.join(cur_dir + "/data/" + file)

    with open(path_to_file, encoding="utf-8") as f:
        transaction = json.load(f)
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


def table_to_dict_list(file: str) -> Any:
    """
    Принимает на вход таблицу трансакций в формате csv или excel и
    возвращает список словарей, отражающих трансакцию в формате
    настоящего проекта.
    :param file:
    :return Any:
    """
    cur_dir = os.path.dirname(os.path.dirname(__file__))
    path_to_file = os.path.join(cur_dir + "/data/" + file)
    ext = os.path.splitext(path_to_file)[1]
    if ext == ".csv":
        df = pd.read_csv(path_to_file, delimiter=";", encoding="utf-8")

    elif ext == ".xls" or ext == ".xlsx":
        df = pd.read_excel(path_to_file)

    else:
        logger.error("Файл с таким расширением не поддерживается")
        return None

    df = df.loc[df["id"] > 0]
    df = df.fillna("unknown_source")
    df = df.rename(columns={"currency_name": "name", "currency_code": "code"})

    currency = df.loc[:, ["name", "code"]].to_dict(orient="records")
    operationAmount = df.loc[:, ["amount"]].to_dict(orient="records")
    operationAmount = [
        {"operationAmount": {"amount": am["amount"], "currency": cur}}
        for am, cur in zip(operationAmount, currency)
    ]

    dict_1 = df.loc[:, ["id", "state", "date"]].to_dict(orient="records")
    dict_2 = df.loc[:, ["from", "to", "description"]].to_dict(orient="records")

    trans_list = [dict_1[i] | operationAmount[i] | dict_2[i] for i in range(len(df))]

    logger.info(f"Успешно получены данные из файла {ext}.")

    return trans_list
