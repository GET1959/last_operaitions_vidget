import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

fh = logging.FileHandler("masks.log", mode="w", encoding="utf-8")
fh.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(module)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)

logger.addHandler(fh)


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
            card_masked = card_masked + " " + new_string[i: i + 4]
        logger.info(f"Создана маска карты {card_number}")
        return card_masked

    else:
        logger.error("Неудачная попытка создания маски карты.")
        return "Неверно введен номер!"


def account_masker(account_number: str) -> str:
    """
    Функция принимает на вход номер счёта и возвращает его маску,
    номер счёта замаскирован и отображается в формате **XXXX.
    :param account_number:
    :return: account_masked:
    """
    if account_number.isdigit() and len(account_number) == 20:
        logger.info(f"Создана маска счета {account_number}")
        return "**" + account_number[-4:]
    else:
        logger.error("Неудачная попытка создания маски счета.")
        return "Неверно введен номер!"
