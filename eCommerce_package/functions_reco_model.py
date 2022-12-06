from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

def get_data_2(path_df1,path_df2):
    df_1 = pd.read_csv(path_df1)
    df_2 = pd.read_csv(path_df2)
    return (df_1, df_2)

def recommendation_model( product_id, df_1, df_2, weight_features = 0.8):
    latent_df_1 = df_1
    latent_df_2 = df_2
    # Get the latent vectors for "Toy Story" from content and collaborative matrices
    v1 = np.array(latent_df_1.loc[product_id]).reshape(1, -1)
    v2 = np.array(latent_df_2.loc[product_id]).reshape(1, -1)

    # Compute the cosine similarity of this movie with the others in the list
    sim1 = cosine_similarity(latent_df_1, v1).reshape(-1)
    sim2 = cosine_similarity(latent_df_2, v2).reshape(-1)

    dictDf_1 = {'features': sim1}
    recommendation_df_1 = pd.DataFrame(dictDf_1, index = latent_df_1.index)

    dictDf_2 = {'ratings': sim2}
    recommendation_df_2 = pd.DataFrame(dictDf_2, index = latent_df_2.index)

    recommendation_combined = pd.merge(recommendation_df_1, recommendation_df_2,
                        left_index=True,
                        right_index=True)
    recommendation_combined['hybrid'] = ((weight_features*recommendation_combined['features']
                                        + (1-weight_features)*recommendation_combined['ratings']))
    recommendation_combined.sort_values('ratings', ascending=False, inplace=True)
    return recommendation_combined


def top_n_products(rec_df, meta_df, n=10, ranking='hybrid'):

    """Valid inputs for ranking: 'features', 'ratings', 'hybrid'"""

    feat_idx = rec_df.sort_values(ranking, ascending=False).index

    counter = 0

    product_ids=[]
    metas=[]
    prices=[]

    for i in feat_idx:
        meta_text = meta_df[meta_df['product_id'] == i][['metadata']].iloc[0,:][0]
        price = meta_df[meta_df['product_id'] == i][['price']].iloc[0,:][0]

        product_ids.append(i)
        metas.append(meta_text)
        prices.append(price)

        counter += 1

    new_df = pd.DataFrame({'product_id':product_ids, 'meta_text':metas, 'price':prices}).drop_duplicates('meta_text').iloc[:n,:]

    return new_df.reset_index().drop(columns='index')


if __name__ == '__main__':
    product_id=5100337
    path_df1 = '../data/latent_dec_19/latent_df_1_with_0.25_data_50_svd_components.csv'
    path_df2 = '../data/latent_dec_19/latent_df_2_with_0.25_data_200_svd_components.csv'
    df_1, df_2 = get_data_2(path_df1,path_df2)
    rec_df = recommendation_model(product_id, df_1, df_2, weight_features = 0.8)
    meta_df = '../data/X_meta2019-Dec.csv_10%.csv'
    new_df = top_n_products(rec_df, meta_df, n=10, ranking='features')
