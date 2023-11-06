from collections.abc import Generator


def filter_by_currency(transactions: list[dict], cur: str) -> Generator:
    """
    Функция принимает список словарей (или объект, который выдает
    по одной словари с транзакциями), и возвращает итератор,
    который выдает по очереди операции, в которых указана заданная валюта.
    :param transactions:
    :param cur:
    :yielded selected transactions:
    """
    cur_transaction = [
        transaction
        for transaction in transactions
        if transaction["operationAmount"]["currency"]["code"] == cur
    ]
    for transact in cur_transaction:
        yield transact


def get_description(transactions: list[dict]) -> Generator:
    """
    Генератор принимает список словарей и возвращает описание каждой операции по очереди.
    :param transactions:
    :yielded descriptions:
    """
    for transact in transactions:
        yield transact["description"]


def card_number_generator(start: int, end: int) -> Generator:
    """
    Генератор номеров банковских карт. Генерирует номера карт
    в формате "XXXX XXXX XXXX XXXX", где X — цифра.
    :rtype: object
    :param start:
    :param end:
    :yielded:
    """

    for i in range(start - 1, end):
        if end > 9999999999999999:
            raise ValueError("Введен слишком длинный номер!")
        if start <= 0:
            raise ValueError("Номер не может быть меньше 1!")
        str_num = "0" * (16 - len(str(i))) + str(i + 1)
        card_number = str_num[:4]
        for j in range(4, len(str_num), 4):
            card_number = card_number + " " + str_num[j: j + 4]
        yield card_number
