def get_selected_list(list_origin: list[dict], state_value: str = "EXECUTED") -> list[dict]:
    """
    Функция принимает на вход список словарей и значение для ключа state
    (опциональный параметр со значением по умолчанию EXECUTED) и возвращает новый список,
    содержащий только те словари, у которых ключ state содержит
    переданное в функцию значение state_value.
    :param list_origin:
    :param state_value:
    :return selected_list:
    """
    selected_list = [op for op in list_origin if op["state"] == state_value]
    return selected_list


def get_sorted_list(list_origin: list[dict], reverse: bool = True) -> list[dict]:
    """
    Функция принимает на вход список словарей и возвращает новый список,
    в котором исходные словари отсортированы по убыванию даты (ключ date).
    Функция принимает два аргумента, второй необязательный
    задает порядок сортировки (убывание, возрастание).
    :param list_origin:
    :param reverse:
    :return sorted_list:
    """
    sorted_list = sorted(list_origin, key=lambda x: x["date"], reverse=reverse)
    return sorted_list
