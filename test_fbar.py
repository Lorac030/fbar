# test_project.py
# Carolina Lovato

from fbar import get_exchange_rate
from fbar import calculate_total_balance_in_USD
from fbar import get_total_foreign_balance


# test get_exchange_rate
def test_get_exchange_rate():
    assert get_exchange_rate('Brazil', 'Real', '2021') == 5.668
    assert get_exchange_rate('Brazil', 'Real', '2011') == 1.85
    assert get_exchange_rate('Brazil', 'Real', '2022') != 4
    assert get_exchange_rate('Canada', 'Dollar', '2021') == 1.277


# test calculate_total_balance_in_USD
def test_calculate_total_balance_in_USD():
    assert calculate_total_balance_in_USD(10,5) == 2
    assert calculate_total_balance_in_USD(100,2) == 50
    assert calculate_total_balance_in_USD(100,0) is None
    assert calculate_total_balance_in_USD(-100,10) == 0


# test get_total_foreign_balance
def test_get_total_foreign_balance():
    # valid bank_data structure
    bank_data = [
        ["2010", "Itau1", 100, 50],
        ["2010", "Itau2", 200, 60],
        ["2010", "Itau3", 300, 70],
    ]
    assert get_total_foreign_balance(bank_data) == 600


# test get_total_foreign_balance for errors
def test_get_total_foreign_balance_fail():
    # INVALID bank_data structure
    bank_data = [
        ["2010", "Itau1", "cat", 50],
        ["2010", "Itau2", "horse", 60],
        ["2010", "Itau3", "300", 70],
    ]
    assert get_total_foreign_balance(bank_data) == 0