import pandas as pd
import numpy as np


def read_clean_data(filename: str):
    return pd.read_csv(filename).drop(['Unnamed: 0', 'QTR_ID'], axis=1)


# Look at historical data to test against
TEST_DATA_LOCATION = 'data/2005-03_sales.csv'
TEST_DATA = read_clean_data(TEST_DATA_LOCATION)
TEST_MIN_VARIABLES = ['ORDERNUMBER', 'ORDERLINENUMBER']
TEST_CONTINUOUS_VARIABLES = ['QUANTITYORDERED', 'PRICEEACH', 'SALES', 'MSRP']


def test_avg_statistics(standard_deviations = 2.96):
    test_data = TEST_DATA[TEST_CONTINUOUS_VARIABLES]
    test_data_means = pd.DataFrame(test_data.mean(axis=0)).T
    test_data_stds_plus = standard_deviations * pd.DataFrame(test_data.std(axis=0)).T
    test_data_stds_minus = -standard_deviations * pd.DataFrame(test_data.std(axis=0)).T
    test_data_high = pd.concat([test_data_means, test_data_stds_plus]).sum()
    test_data_low = pd.concat([test_data_means, test_data_stds_minus]).sum()
    return {'upper_bound': dict(test_data_high), 'lower_bound': (test_data_low)}



def test_columns_and_data_type(new_data: pd.DataFrame):
    try:
        pd.testing.assert_frame_equal(TEST_DATA.iloc[0:0], new_data[0:0], check_like=True)
        print('[SUCCESS] - dataframes have same columns and dtypes')
        return True
    except Exception as e:
        print(f'[ERROR] - an exception was thrown: {e}')
        return False


def test_gte_min_variables(new_data: pd.DataFrame):
    try:
        n_tests = len(TEST_MIN_VARIABLES)
        n_correct = 0
        for variable in TEST_MIN_VARIABLES:
            min_test_data = min(TEST_DATA[variable])
            min_data = min(new_data[variable])
            if min_data >= min_test_data:
                print(f'[SUCCESS] - All {variable} >= minimum requirement')
                n_correct += 1
            else:
                print(f'[ERROR] - All {variable} not >= minimum requirement')
        if n_correct == n_tests:
            return True
        else:
            return False
    except Exception as e:
        print(f'[ERROR] - an exception was thrown: {e}')
        return False


def test_continuous_outlier_variables(new_data: pd.DataFrame):
    try:
        TEST_AVG_STATISTICS = test_avg_statistics()
        n_tests = len(TEST_CONTINUOUS_VARIABLES)
        n_correct = 0
        for variable in TEST_CONTINUOUS_VARIABLES:
            if (new_data[variable] < TEST_AVG_STATISTICS['lower_bound'][variable]).all() or \
                    (new_data[variable] > TEST_AVG_STATISTICS['upper_bound'][variable]).all():
                print(f'[ERROR] - {variable} - does not fit the outlier requirements!')
            else:
                print(f'[SUCCESS] - {variable} - fits the outlier requirements!')
                n_correct += 1
        if n_correct == n_tests:
            return True
        else:
            return False
    except Exception as e:
        print(f'[ERROR] - an exception was thrown: {e}')
        return False

