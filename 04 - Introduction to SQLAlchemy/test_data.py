from os import listdir
import pandas as pd
from utils import read_clean_data, test_columns_and_data_type, test_gte_min_variables, test_continuous_outlier_variables


def test_data_integrity(new_data: pd.DataFrame):
    my_test_results = dict()

    # Run tests and append results to dictionary
    cols_and_dtype = test_columns_and_data_type(new_data)
    my_test_results['cols_and_dtype'] = cols_and_dtype

    gte_min = test_gte_min_variables(new_data)
    my_test_results['gte_min'] = gte_min

    outlier_variables = test_continuous_outlier_variables(new_data)
    my_test_results['outlier_variables'] = outlier_variables

    for i in my_test_results.items():
        print(f'TEST: {i[0]}  ----> PASS: {i[1]}')

    if all(my_test_results.values()):
        return True
    else:
        return False

