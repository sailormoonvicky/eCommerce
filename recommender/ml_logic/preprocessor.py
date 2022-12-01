import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity

def preprocessing_feat(X: pd.DataFrame, drop_event_time=False) -> pd.DataFrame:
    """
    Create a scikit-learn preprocessor
    that transforms a cleaned dataset of shape (_, 7)
    into a preprocessed one of different fixed shape (_, 65)
    """
    if drop_event_time:
        X = X.drop("event_time", axis=1)

    X_preprocessed = X.dropna(subset = ['category_code', 'brand']) #tbd!!
    X_preprocessed = X_preprocessed.drop_duplicates()
    X_preprocessed['category_code'] = X_preprocessed['category_code'].str.replace('.',' ')
    return X_preprocessed
