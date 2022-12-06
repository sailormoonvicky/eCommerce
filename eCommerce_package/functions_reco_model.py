from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

def get_data_2():
    path_df1 = '../data/Oct19_20/latent_df_1_with_100pct_data_50_svd_components_oct19.csv'
    path_df2 = '../data/Oct19_20/latent_df_2_with_100pct_data_100_svd_components_oct19.csv'
    path_df3 = '../data/Oct19_20/X_meta_with_100pct_data_oct19.csv'
    df_1 = pd.read_csv(path_df1,index_col=[0])
    df_2 = pd.read_csv(path_df2,index_col=[0])
    meta_df = pd.read_csv(path_df3, index_col=[0])
    return (df_1, df_2, meta_df)

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
        # import ipdb; ipdb.set_trace()
        meta_text = meta_df[meta_df['product_id.1'] == i][['metadata']].iloc[0,:][0]
        price = meta_df[meta_df['product_id.1'] == i][['price']].iloc[0,:][0]

        product_ids.append(i)
        metas.append(meta_text)
        prices.append(price)

        counter += 1

    new_df = pd.DataFrame({'product_id.1':product_ids, 'meta_text':metas, 'price':prices}).drop_duplicates('meta_text').iloc[:n,:]

    return new_df.reset_index().drop(columns='index')


if __name__ == '__main__':
    try:
        # 1003363 1002544
        product_id= 1000978
        df_1, df_2, meta_df = get_data_2()
        # print("Starting recommendation model")
        rec_df = recommendation_model(product_id, df_1, df_2, weight_features = 0.8)
        # print("Starting product sorting")
        new_df = top_n_products(rec_df, meta_df, n=10, ranking='features')
        # print(new_df.head())

    except:
        import ipdb, traceback, sys
        extype, value, tb = sys.exc_info()
        traceback.print_exc()
        ipdb.post_mortem(tb)
