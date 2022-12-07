import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="eCommerce Rercommender", # => The title
    page_icon="🛒",
    layout="wide", # wide
    initial_sidebar_state="auto") # collapsed

##########################################
##  Load and Prep Data                  ##
##########################################

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

st.title("Let's go shopping!")
st.markdown('''##### <span style="color:gray">Predict consumer preference and recommend related products</span>
            ''', unsafe_allow_html=True)

cols_1, cols_2, cols_3 = st.sidebar.columns([1,8,1])
with cols_1:
    st.write("")
with cols_2:
    st.image('data_streamlit/ecommerce.png',  use_column_width=True)
with cols_3:
    st.write("")

st.sidebar.markdown(" ## About eCommerce Recommender")
st.sidebar.markdown("1️⃣ model based on cusumer preference places 16k+ products into 3000+ brands buckets.")
st.sidebar.markdown('2️⃣ model finds the feature based similar produts to each single product.')
st.sidebar.markdown('3️⃣ model predicts the most suitable corssed products of each single.')
st.sidebar.info("Read more about how the model works and see the code on our [Github](https://github.com/sailormoonvicky/eCommerce).", icon="ℹ️")

col1, col2,col3, col4, col5 = st.columns(5)

tab_start, tab_samsung, tab_apple, tab_huawei, tab_lg, tab_lenovo = st.tabs(['Start', 'Samsung', 'Apple', 'Huawei', 'LG', 'Lenovo'])
with col1:
    image = Image.open('data_streamlit/{}.png'.format(brands[0]))
    st.image(image, caption='{}'.format(brands[0]))

with col2:
    image = Image.open('data_streamlit/{}.png'.format(brands[1]))
    st.image(image, caption='{}'.format(brands[1]))

with col3:
    image = Image.open('data_streamlit/{}.png'.format(brands[2]))
    st.image(image, caption='{}'.format(brands[2]))

with col4:
    image = Image.open('data_streamlit/{}.png'.format(brands[3]))
    st.image(image, caption='{}'.format(brands[3]))

with col5:
    image = Image.open('data_streamlit/{}.png'.format(brands[4]))
    st.image(image, caption='{}'.format(brands[4]))

with tab_start:
    st.write('Welcome!')
    st.markdown('Contributors: Christian Jergen,Héléna Antoniadis, Zhenghan Hu')
    st.markdown('Supervisors: Julio Quintana, Lorcan Rae')


##########################################
## Tab                                  ##
##########################################

def expand_brand(i):
    expand_brand = st.expander("Best sellers of {}".format(brands[i]), expanded=False)
    with expand_brand:
        product = st.selectbox("Find the best sellers of {}:".format(brands[i]), df[df.brand==brands[i].lower()].product_id)
        st.write(f'''
            ###### <div style="text-align: center"> According to our model, </span> </div>


            ###### <div style="text-align: center"> <span style="color:indianred">[{product}] </span> is one of the Best sellers of <span style="color:indianred">  {brands[i]} </span> in 2020-2021.</span> </div>
            ''', unsafe_allow_html=True)
        col1_1,col1_2,col1_3=st.columns(3)
        with col1_1:
            st.write('')

        with col1_2:
            st.image(f'data_streamlit/{df[df.product_id==product].metadata.tolist()[0]}.png')

        with col1_3:
            st.write('')

        styler_product = df[df.product_id == product][cols].style.pipe(make_pretty)

        return st.table(styler_product)


def expand_similarity():
    expand_similarity = st.expander("Similar recommender you maybe like")
    with expand_similarity:

        #number slider
        slider1, slider2 = st.columns([4,10])
        with slider1:
            num_entries = st.slider('Number of recommenders to show:', 0, 10, 5, step =5)
        with slider2:
            st.write('')
        st.write(f'''
                ##### <div style="text-align: center"> According to our model, you maybe like these: </span> </div>
                ''', unsafe_allow_html=True)

        #select the recommender to check the crossed recommended pruducts
        recommend_df = df[cols][:num_entries]
        recommender = st.selectbox("Select the product you're interested:", recommend_df.product_id)

        recommend_styler = recommend_df.style.pipe(make_pretty)
        st.table(recommend_styler)

        st.write(f'''
                ##### <div style="text-align: center"> According to our model, you maybe also like these: </span> </div>
                ##### <div style="text-align: center"> Crossed products recommender: </span> </div>
                ''', unsafe_allow_html=True)

        cross_df = df[df.product_id == recommender][cols][:10]
        cross_styler = cross_df.style.pipe(make_pretty)
        st.table(cross_styler)



with tab_samsung:
    expand_brand(0)

###################

    expand_similarity()


###################


with tab_apple:
    expand_brand(1)

###################
    expand_similarity = st.expander("Similar recommender you maybe like")
    with expand_similarity:
        st.write(f'''
                ##### <div style="text-align: center"> According to our model, you maybe like these: </span> </div>
                ''', unsafe_allow_html=True)

        recommend_df = df[cols][:10]
        recommend_styler = recommend_df.style.pipe(make_pretty)
        st.table(recommend_styler)

###################
    expand_cross = st.expander("Crossed products recommender")
    with expand_cross:
        st.write(f'''
                ##### <div style="text-align: center"> According to our model, you maybe also like these: </span> </div>
                ''', unsafe_allow_html=True)

        cross_df = df[cols][10:30]
        cross_styler = cross_df.style.pipe(make_pretty)
        st.table(cross_styler)

with tab_huawei:
    expand_brand(2)

###################
    expand_similarity = st.expander("Similar recommender you maybe like")
    with expand_similarity:
        st.write(f'''
                ##### <div style="text-align: center"> According to our model, you maybe like these: </span> </div>
                ''', unsafe_allow_html=True)

        recommend_df = df[cols][:10]
        recommend_styler = recommend_df.style.pipe(make_pretty)
        st.table(recommend_styler)

###################
    expand_cross = st.expander("Crossed products recommender")
    with expand_cross:
        st.write(f'''
                ##### <div style="text-align: center"> According to our model, you maybe also like these: </span> </div>
                ''', unsafe_allow_html=True)

        cross_df = df[cols][10:30]
        cross_styler = cross_df.style.pipe(make_pretty)
        st.table(cross_styler)


with tab_lg:
    expand_brand(3)

###################
    expand_similarity = st.expander("Similar recommender you maybe like")
    with expand_similarity:
        st.write(f'''
                ##### <div style="text-align: center"> According to our model, you maybe like these: </span> </div>
                ''', unsafe_allow_html=True)

        recommend_df = df[cols][:10]
        recommend_styler = recommend_df.style.pipe(make_pretty)
        st.table(recommend_styler)

###################
    expand_cross = st.expander("Crossed products recommender")
    with expand_cross:
        st.write(f'''
                ##### <div style="text-align: center"> According to our model, you maybe also like these: </span> </div>
                ''', unsafe_allow_html=True)

        cross_df = df[cols][10:30]
        cross_styler = cross_df.style.pipe(make_pretty)
        st.table(cross_styler)

with tab_lenovo:
    expand_brand(4)

###################
    expand_similarity = st.expander("Similar recommender you maybe like")
    with expand_similarity:
        st.write(f'''
                ##### <div style="text-align: center"> According to our model, you maybe like these: </span> </div>
                ''', unsafe_allow_html=True)

        recommend_df = df[cols][:10]
        recommend_styler = recommend_df.style.pipe(make_pretty)
        st.table(recommend_styler)

###################
    expand_cross = st.expander("Crossed products recommender")
    with expand_cross:
        st.write(f'''
                ##### <div style="text-align: center"> According to our model, you maybe also like these: </span> </div>
                ''', unsafe_allow_html=True)

        cross_df = df[cols][10:30]
        cross_styler = cross_df.style.pipe(make_pretty)
        st.table(cross_styler)
