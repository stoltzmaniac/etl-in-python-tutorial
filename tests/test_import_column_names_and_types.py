import sys


def test_data(historical_data):
    print(historical_data.head())
    assert len(historical_data) > 0


def test_no():
    assert True == True
