import pytest

from src.masks import card_masker, account_masker


@pytest.mark.parametrize("card_number, expected",
                         [('4562789536587512', '4562 78** **** 7512'),
                          ('0000000536580000', '0000 00** **** 0000'),
                          ('456278953658751', 'Неверно введен номер!'),
                          ('45627895abc8751', 'Неверно введен номер!'),
                          ('45627895abc87512', 'Неверно введен номер!')])
def test_card_masker(card_number: str, expected: list):
    assert card_masker(card_number) == expected

@pytest.mark.parametrize("account_number, expected",
                         [('12365478936985214723', '**4723'),
                          ('32741258963987400000', '**0000'),
                          ('3274125896398745632', 'Неверно введен номер!'),
                          ('327412589639874563212', 'Неверно введен номер!'),
                          ('327412589639874566abc', 'Неверно введен номер!')])
def test_account_masker(account_number: str, expected: list):
    assert account_masker(account_number) == expected