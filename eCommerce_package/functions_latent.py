import os
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD


def get_data(path):
    p=0.01
    df = pd.read_csv(
         path,
         header=0,
         skiprows=lambda i: i>0 and random.random() > p)
    filename = os.path.basename(path)
    return (df,filename)

#  for Similar_product_recommender - Latent_matrix_from_metadata - latent_df_1

def preprocessing_feat(df, drop_event_time=True):
    if drop_event_time:
        df = df.drop("event_time", axis=1)

    X_preprocessed = df.dropna(subset = ['category_code', 'brand'])
    X_preprocessed = X_preprocessed.drop_duplicates()
    X_preprocessed['category_code'] = X_preprocessed['category_code'].str.replace('.',' ')
    return X_preprocessed

#  for Similar_product codes - Pricing_criterion

def make_column(row):
    if row["price"] < row["25%"]:
        return "low"
    elif row["price"] < row["75%"]:
        return "medium"
    else:
        return "high"

def pricing_criterion(X_preprocessed):
    pricing_guide = X_preprocessed.groupby('category_code')['price'].describe()[["25%", "75%"]].reset_index()
    X_merged = X_preprocessed.merge(pricing_guide, on="category_code", how="right")
    X_merged["price_category"] = X_merged.apply(lambda row: make_column(row), axis=1)
    return X_merged

def metadata(X_merged):
    X_merged['metadata'] = X_merged[['category_code', 'brand', 'price_category']].apply(lambda x: ' '.join(x), axis = 1)
    X_merged.set_index(X_merged['product_id'], inplace=True)
    X_meta=X_merged
    X_meta.to_csv(os.path.join('..','data',f'X_meta{filename}'), index=False)
    return X_meta

def count_vectorizer(X_meta):
    count = CountVectorizer()
    count_matrix = count.fit_transform(X_meta['metadata'])
    count_df_1 = pd.DataFrame(count_matrix.toarray(), index=X_meta.product_id.tolist())
    return count_df_1

def count_vectorizer_prepro (count_df_1):
    count_df_1 = count_df_1.reset_index()
    count_df_1.drop_duplicates(subset='index', keep='first', inplace=True)
    count_df_1["product_id"] = count_df_1["index"]
    count_df_1.drop("index", axis=1, inplace=True)
    return count_df_1

def dimensionality_reduction_df1 (count_df_1,n=50):
    svd = TruncatedSVD(n_components=n)
    latent_df_1_pre = svd.fit_transform(count_df_1.set_index("product_id"))
    return latent_df_1_pre

def latent_df_1_csv (latent_df_1_pre):
    df_for_latent1 = latent_df_1_pre.product_id.tolist()
    latent_df_1 = pd.DataFrame(latent_df_1_pre[:,0:n], index=df_for_latent1)
    latent_df_1.reset_index().drop_duplicates() #.shape
    latent_df_1.to_csv(os.path.join('..','data',f'latent_df_1_{filename}'), index=False)
    return latent_df_1

### return first latent df ####

#  for Similar_product_recommender - Latent matrix from event types - latent_df_2

def preprocessing_event(df):
    X_preprocessed = df.dropna(subset = ['category_code', 'brand']) #tbd!!
    df_event = X_preprocessed.drop_duplicates()
    return df_event

def session_rating (df_event):
    dct = {'view': 1, 'cart': 3, 'purchase': 5}
    df_event['rating'] = df_event['event_type'].map(dct)
    df_event.drop_duplicates(subset='product_id',inplace=True)
    df_rating = df_event.pivot(values='rating',
               index='product_id',
               columns='user_id').fillna(0)
    return df_rating.reset_index()

# def rating_prepro (df_rating):
#     df_rating.sum().reset_index()[0].sum()
#     df_event.groupby("user_id").agg({"rating":sum}).sort_values(by="rating").sum()
#     df_event.groupby("user_id").agg({"rating":sum}).sort_values(by="rating").sum()
#     return df_rating.reset_index()

def dimensionality_reduction_df2 (df_rating,n=75):
    svd = TruncatedSVD(n_components=75)
    latent_df_2 = svd.fit_transform(df_rating)
    latent_df_2 = pd.DataFrame(latent_df_2, index=df_rating.reset_index().product_id.tolist())
    latent_df_2.to_csv(os.path.join('..','data',f'latent_df_2_{filename}'), index=False)
    return latent_df_2

### return second latent df ####


def top_n_products(product_id, rec_df, meta_df, n=10, ranking='hybrid'):

    """Valid inouts for ranking: 'features', 'ratings', 'hybrid'"""

    feat_idx = rec_df.sort_values(ranking, ascending=False).index[0:n]
    counter = 0

    for i in feat_idx:
        meta_text = meta_df[meta_df['product_id'] == i][['metadata']].iloc[0,:][0]

        if counter == 0:
            print(f"Top {n} recommendations for product_id {product_id}:")
            print(f"{i} - {meta_text} \n")
#             print("-----------------------")

        else:
            print(f"Rec {counter}) {i} - {meta_text}")

        counter += 1


if __name__ == '__main__':
    some_path = '../data/10%sample/2019-Dec.csv_10%.csv'
    df,filename = get_data(some_path) #specify the weight of the data to use
    X_preprocessed = preprocessing_feat(df)
    X_merged = pricing_criterion(X_preprocessed)
    X_meta = metadata(X_merged)
    # breakpoint()
    count_df_1 = count_vectorizer(X_meta)
    count_df_1 = count_vectorizer_prepro(count_df_1)
    latent_df_1_pre = dimensionality_reduction_df1(count_df_1,n=50)
    latent_df_1 = latent_df_1_csv(latent_df_1_pre)
    ### latent_df1 created and saved as csv

    df_event = preprocessing_event(df)
    df_rating = session_rating(df_event)
    latent_df_2 = dimensionality_reduction_df2(df_rating,n=75)
    ### latent_df2 created and saved as csv
