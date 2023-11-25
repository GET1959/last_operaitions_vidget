import logging
import os
import re
from collections import Counter
from typing import Any

import pandas as pd


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

fh = logging.FileHandler("utils.log", mode="w", encoding="utf-8")
fh.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(module)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)

logger.addHandler(fh)


def table_to_dict_list(file: str) -> Any:
    """
    Принимает на вход таблицу трансакций в формате csv или excel и
    возвращает список словарей, отражающих трансакцию в формате
    настоящего проекта.
    :param file:
    :return Any:
    """
    cur_dir = os.path.dirname(os.path.abspath("."))
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


transact_list = table_to_dict_list("transactions_excel.xlsx")
print(category_count(transact_list))
# for i in range(len(find_operation(transact_list, 'Открытие вклада'))):
#     print(find_operation(transact_list, 'Открытие вклада')[i])
find_operation(transact_list, "Открытие")
print([trans for trans in transact_list if "Открытие" in trans["description"]])
