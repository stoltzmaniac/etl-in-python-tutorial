import pytest
import pandas as pd


class SETUP:
    """
    Used for conftest.py in order to allow for easy access to changes in directory structure
    """
    def __init__(self):
        pass
    historical_data_location = "data/2003-2004_sales.csv"


@pytest.fixture
def historical_data():
    df = pd.read_csv(SETUP.historical_data_location)
    assert len(df) > 0
    return df

