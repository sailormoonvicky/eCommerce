import streamlit as st
from PIL import Image
import pandas as pd

from eCommerce_package.functions_reco_model import get_data_2, recommendation_model, top_n_products

st.set_page_config(
    page_title="eCommerce Rercommender", # => The title
    page_icon="🛒",
    layout="wide", # wide
    initial_sidebar_state="auto") # collapsed

##########################################
##  Load and Prep Data                  ##
##########################################
df_1, df_2, meta_df = get_data_2(local=False)

@st.cache
def load_data():
    df = pd.read_csv('top25.csv')
    return df

df = load_data()

brands=['Samsung', 'Apple', 'Huawei', 'LG', 'Lenovo']
cols = ['product_id','category_code','brand','price', 'price_category']

##########################################
##  Style and Formatting                ##
##########################################

hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>   """

center_heading_text = """
    <style>
        .col_heading   {text-align: center !important}
    </style>          """

center_row_text = """
    <style>
        td  {text-align: center !important}
    </style>      """

# Inject CSS with Markdown

st.markdown(hide_table_row_index, unsafe_allow_html=True)
st.markdown(center_heading_text, unsafe_allow_html=True)
st.markdown(center_row_text, unsafe_allow_html=True)

brands=['Samsung', 'Apple', 'Huawei', 'LG', 'Lenovo']
cols = ['product_id','category_code','brand','price', 'price_category']

heading_properties = [('font-size', '16px'),('text-align', 'center'),
                      ('color', 'white'),  ('font-weight', 'bold'),
                      ('background', 'gray'),('border', '1.2px solid black')]

cell_properties = [('font-size', '16px'),('text-align', 'center')]

# definite the styler function
dfstyle = [{"selector": "th", "props": heading_properties},
               {"selector": "td", "props": cell_properties}]

def make_pretty(styler):
    styler.set_properties(**{'background': 'mistyrose', 'border': '1.2px solid'})
    styler.hide(axis='index')
    styler.set_table_styles(dfstyle)
    styler.format(precision=2)
    return styler

##########################################
##  Title, Tabs, and Sidebar            ##
##########################################

st.title("Let's start your shopping journey!")
st.markdown('''##### <span style="color:gray">Our 5 most popular brands</span>
            ''', unsafe_allow_html=True)
st.write('')

cols_1, cols_2, cols_3 = st.sidebar.columns([1,8,1])
with cols_1:
    st.write("")
with cols_2:
    st.image('data_streamlit/ecommerce.png',  use_column_width=True)
with cols_3:
    st.write("")

st.sidebar.markdown(" ## About eCommerce Recommender")
st.sidebar.markdown('''1️⃣ <span style="font-weight:bold">Catch attention</span>''', unsafe_allow_html=True)
st.sidebar.markdown("    Display best seller products for popular brands")
st.sidebar.markdown('''2️⃣ <span style="font-weight:bold">Facilitate choice</span>''', unsafe_allow_html=True)
st.sidebar.markdown("    Provide relevant and meaningful selection of products")
st.sidebar.markdown('3️⃣ <span style="font-weight:bold">Enrich basket</span>', unsafe_allow_html=True)
st.sidebar.markdown("    Identify cross selling product option")
st.sidebar.markdown('Contributors: Zhenghan Hu, Héléna Antoniadis, Christian Jergen')
st.sidebar.markdown('Supervisors: Julio Quintana, Lorcan Rae')
st.sidebar.info("Read more about how the model works and see the code on our [Github](https://github.com/sailormoonvicky/eCommerce).", icon="ℹ️")

col1, col2,col3, col4, col5 = st.columns(5)

st.write('')
tab_start, tab_samsung, tab_apple, tab_huawei, tab_lg, tab_lenovo, tab_cross = st.tabs(['Start', 'Samsung', 'Apple', 'Huawei', 'LG', 'Lenovo', 'Enrich Basket'])
with col1:
    image = Image.open('data_streamlit/{}.png'.format(brands[0]))
    st.image(image)#, caption='{}'.format(brands[0]))

with col2:
    image = Image.open('data_streamlit/{}.png'.format(brands[1]))
    st.image(image)

with col3:
    image = Image.open('data_streamlit/{}.png'.format(brands[2]))
    st.image(image)

with col4:
    image = Image.open('data_streamlit/{}.png'.format(brands[3]))
    st.image(image)

with col5:
    image = Image.open('data_streamlit/{}.png'.format(brands[4]))
    st.image(image)

with tab_start:
    st.write('')



##########################################
## Tab                                  ##
##########################################

def expand_brand(i):
    st.write(f'''
            ###### <div style="text-align: center"> Top 5 products of <span style="color:indianred"> {brands[i]} </span> : </span> </div>
            ''', unsafe_allow_html=True)
    brand_df = df[df.brand==brands[i].lower()][cols]
    brand_df.rename(columns={'category_code': 'Description', 'brand':'Brand','product_id':'Product ID', 'price':'Price', 'price_category':'Price category'}, inplace=True)
    brand_df.Brand=brand_df.Brand.apply(lambda x: x.upper())
    st.table(brand_df.style.pipe(make_pretty))

    st.write("Continue to find more details")

    expand_brand = st.expander("Find the best sellers of {}:".format(brands[i]), expanded=False)

    with expand_brand:
        product = st.selectbox('Select:', df[df.brand==brands[i].lower()].product_id)
        st.write(f'''
            ###### <div style="text-align: center"> This product is one of the best sellers of <span style="color:indianred">  {brands[i]} </span> in 2020-2021.</span> </div>
            ''', unsafe_allow_html=True)
        col1_1,col1_2,col1_3=st.columns(3)
        with col1_1:
            st.write('')

        with col1_2:
            st.image(f'data_streamlit/{df[df.product_id==product].metadata.tolist()[0]}.png')

        with col1_3:
            st.write('')

        st.write(f'''
                ##### <div style="text-align: center"> Based on your selection, you may like the following products: </span> </div>
                ''', unsafe_allow_html=True)

        #load recommendation model
        rec_df = recommendation_model(product, df_1, df_2, meta_df, weight_features = 0.8)
        rec_df = top_n_products(rec_df, meta_df, n=10, ranking='features')
        rec_df.rename(columns={'meta_text': 'description'}, inplace=True)

        rec_styler = rec_df.style.pipe(make_pretty)
        st.table(rec_styler)


with tab_samsung:
    expand_brand(0)

with tab_apple:
    expand_brand(1)

with tab_huawei:
    expand_brand(2)

with tab_lg:
    expand_brand(3)

with tab_lenovo:
    expand_brand(4)

with tab_cross:
    df_x_seller = pd.read_csv('x_seller.csv')
    st.write(f'''
            ###### <div style="text-align: center"> Based on your previous purchase, you may like one of the products below: </span> </div>
            ''', unsafe_allow_html=True)
    c_product = st.selectbox("Select the product you're interested in:", df_x_seller.product_1)
    cros_df = df_x_seller[df_x_seller['product_1']==c_product][['product_1','price_1','metadata_1','product_2','price_2','metadata_2']]
    cros_df.rename(columns={'product_1':'target product', 'product_2': 'recommend product', 'price_1':'target price', 'price_2': 'recommender price', 'metadata_1':'target description','metadata_2':'recommender description' }, inplace=True)
    st.table(cros_df.style.pipe(make_pretty))
