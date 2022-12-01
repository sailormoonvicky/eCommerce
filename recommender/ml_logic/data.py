import pandas as pd
import numpy as np

def clean_data(X: pd.DataFrame, drop_event_time=False) -> pd.DataFrame:
    """
    clean raw data by removing buggy or irrelevant transactions
    or columns for the training set
    """
    if drop_event_time:
        X = X.drop("event_time", axis=1)

    X_preprocessed = X.dropna(subset = ['category_code', 'brand']) #tbd!!
    X_preprocessed = X_preprocessed.drop_duplicates()
    X_preprocessed['category_code'] = X_preprocessed['category_code'].str.replace('.',' ')
    return X_preprocessed

def get_chunk(source_name: str) -> pd.DataFrame:
    """
    Return a `chunk_size` rows from the source dataset, starting at row `index` (included)
    Always assumes `source_name` (local or cloud storage) have headers,
    and do not consider them as part of the data `index` count.
    """





def save_chunk() -> None:
    '''save chunk'''
