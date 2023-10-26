def card_masker(card_number: str) -> str:
    """
    Функция принимает на вход номер карты и возвращает ее маску,
    номер карты замаскирован и отображается в формате XXXX XX** **** XXXX.
    :param card_number:
    :return: card_masked:
    """
    new_string = card_number[:6] + "******" + card_number[-4:]
    if card_number.isdigit() and len(card_number) == 16:
        card_masked = new_string[:4]
        for i in range(4, len(card_number), 4):
            card_masked = card_masked + ' ' + new_string[i:i+4]
        return card_masked

    else:
        return 'Неверный номер карты!'


def account_masker(account_number: str) -> str:
    """
    Функция принимает на вход номер счёта и возвращает его маску,
    номер счёта замаскирован и отображается в формате **XXXX.
    :param account_number:
    :return: account_masked:
    """
    if account_number.isdigit() and len(account_number) == 20:
        return "**" + account_number[-4:]
    else:
        return 'Неверный номер счета!'
