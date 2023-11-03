import pytest

from src.processing import get_selected_list, get_sorted_list

@pytest.fixture()
def lst_origin():
    return [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

@pytest.mark.parametrize("state_value, expected",
                         [("EXECUTED", [{'id': 41428829, 'state': 'EXECUTED',
                                         'date': '2019-07-03T18:35:29.512364'},
                                        {'id': 939719570, 'state': 'EXECUTED',
                                         'date': '2018-06-30T02:08:58.425572'}]),
                          ("CANCELED", [{'id': 594226727, 'state': 'CANCELED',
                                         'date': '2018-09-12T21:27:25.241689'},
                                        {'id': 615064591, 'state': 'CANCELED',
                                         'date': '2018-10-14T08:21:33.419441'}])])
def test_get_selected_list(lst_origin, state_value, expected):
    assert get_selected_list(lst_origin, state_value) == expected


@pytest.mark.parametrize("reverse, expected", [(True, [
             {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
             {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
             {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
             {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]),
    (False, [{'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
             {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
             {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
             {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}])])
def test_get_sorted_list(lst_origin, reverse, expected):
    assert get_sorted_list(lst_origin, reverse) == expected