from typing import Any
from datetime import datetime

from src.masks import account_masker, card_masker


def get_type_and_mask(type_and_number: str) -> Any:
    """
    Функция принимает на вход название и номер карты или счета, введенные через пробел и
    возвращает их тип (строка) и их маску.
    :param type_and_number:
    :return: type and masked number:
    """
    item_type = "".join([i for i in type_and_number if not i.isdigit()])
    item_number = "".join([i for i in type_and_number if i.isdigit()])
    if type_and_number[:4].lower() == "счет":
        account_number_masked = account_masker(item_number)
        if account_number_masked == "Неверно введен номер!":
            return account_number_masked
        else:
            return f"{item_type}{account_number_masked}"
    else:
        card_number_masked = card_masker(item_number)
        if card_number_masked == "Неверно введен номер!":
            return card_number_masked
        else:
            return f"{item_type}{card_number_masked}"


def date_str_to_date(str_date: str) -> Any:
    """
    Функция переформатирует дату.
    :param str_date:
    :return str_date_formatted:
    """
    return datetime.strptime(str_date.replace('T', ' '),
                             '%Y-%m-%d %H:%M:%S.%f').strftime('%d.%m.%Y')
