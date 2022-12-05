import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="eCommerce Rercommender", # => The title
    page_icon="🛒",
    layout="wide", # wide
    initial_sidebar_state="auto") # collapsed

@st.cache
def load_data():
    df = pd.read_csv('data/2019_oct_sort_1000.csv')
    return df

df = load_data()

cols = ['product_id','category_code','brand','price']

heading_properties = [('font-size', '16px'),('text-align', 'center'),
                      ('color', 'white'),  ('font-weight', 'bold'),
                      ('background', 'black'),('border', '1.2px solid')]

cell_properties = [('font-size', '16px'),('text-align', 'center')]

dfstyle = [{"selector": "th", "props": heading_properties},
               {"selector": "td", "props": cell_properties}]

st.title("Let's go shopping!")
st.markdown('''##### <span style="color:gray">Predict consumer preference and recommend related products</span>
            ''', unsafe_allow_html=True)

cols_1, cols_2, cols_3 = st.sidebar.columns([1,8,1])
with cols_1:
    st.write("")
with cols_2:
    st.image('data/ecommerce.png',  use_column_width=True)
with cols_3:
    st.write("")

st.sidebar.markdown(" ## About eCommerce Recommender")
st.sidebar.markdown("1️⃣ model based on cusumer preference places 16k+ products into 3000+ brands buckets.")
st.sidebar.markdown('2️⃣ model finds the feature based similar produts to each single product.')
st.sidebar.markdown('3️⃣ model predicts the most suitable corssed products of each single.')
st.sidebar.markdown('Contributors: Christian Jergen,Héléna Antoniadis, Zhenghan Hu')
st.sidebar.markdown('Supervisors: Julio Quintana, Lorcan Rae')
st.sidebar.info("Read more about how the model works and see the code on our [Github](https://github.com/sailormoonvicky/eCommerce).", icon="ℹ️")

def get_select_box_data(product, recommender):
    # Remember to filter by brand here
    return pd.DataFrame(#{f'{brand}': [1,2,3,4,5],
        {'Product': product,
        'Recommender': recommender
        })

# brand = [i if st.session_state[i]==True else None for i in st.session_state][0]

col1, col2,col3, col4, col5 = st.columns(5)

tab_start, tab_apple, tab_samsung, tab_adidas, tab_chanel, tab_nintendo = st.tabs(["Start","Apple", "Samsung", "adidas", "Chanel",'Nintendo'])
# tab_apple, tab_samsung, tab_adidas, tab_chanel, tap_nintendo = st.columns(5)
with col1:
    image = Image.open('data/apple.png')
    st.image(image, caption='Apple')

with col2:
    image = Image.open('data/samsung.png')
    st.image(image, caption='Samsung')

with col3:
    image = Image.open('data/adidas.png')
    st.image(image, caption='adidas')

with col4:
    image = Image.open('data/chanel.png')
    st.image(image, caption='Chanel')

with col5:
    image = Image.open('data/nintendo.png')
    st.image(image, caption='Nintendo')



with tab_start:
    st.write('Welcome!')

with tab_apple:
    product = st.selectbox("Find the best sellers of Apple:", df.product_id, index =10)
    st.write(f'''
         ##### <div style="text-align: center"> In the 2020-21, <span style="color:blue">[{product}] </span> is one of the Best sellers of Apple, xxx have been sold out. </span> </div>

          ##### <div style="text-align: center"> According to our model, you maybe like these: </span> </div>
         ''', unsafe_allow_html=True)
    col1_1,col1_2,col1_3=st.columns(3)
    with col1_1:
        st.write('')

    with col1_2:
        st.image('data/ip.png')

    with col1_3:
        st.write('')

    styler_product = (df[df.product_id == product][cols]
                   .style.set_properties(**{'background': 'azure', 'border': '1.2px solid'})
                   .hide(axis='index')
                   .set_table_styles(dfstyle)
                   )
    st.table(styler_product)

    st.write(f'''
             ##### <div style="text-align: center"> According to our model, you maybe like these: </span> </div>
             ''', unsafe_allow_html=True)

    recommend_df = df[cols][:10].style.set_properties(**{'background': 'azure', 'border': '1.2px solid'}).hide(axis='index').set_table_styles(dfstyle)

    st.table(recommend_df)

    # product = st.selectbox("Find the best sellers of Apple:", df.product_id, index =10)

    # if "apple" not in st.session_state:
    #     st.session_state["apple"] = False

    # if st.button("Check Apple's Products"):
    #     st.session_state["apple"] = not st.session_state["apple"]
    #     st.session_state["samsung"] = False
    #     st.session_state["adidas"] = False
    #     st.session_state["chanel"] = False
    #     st.session_state["nintendo"] = False

    # if st.session_state['apple'] == True:
    #     with st.form(key = 'edit_form_apple'):
    #         # print is visible in the server output, not in the page

    #         product = ['Product1', 'Product2', 'Product3', 'Product4', 'Product5']
    #         recommender = ['r1','r2','r3','r4','r5'], ['r6','r7','r8','r9','r10'], ['r11','r12','r13','r14','r15'], ['r16','r17','r18','r19','r20'],['r21','r22','r23','r24','r25']
    #         df = get_select_box_data(product, recommender)
    #         option = st.selectbox('Select a product', df['Product'])

    #         if st.form_submit_button(label='Product Selected'):
    #             filtered_df = df[df['Product'] == option]
    #             recommender_df = filtered_df['Recommender']
    #             st.write('Recommender')
    #             st.write(recommender_df.iloc[0][0])
    #             st.write(recommender_df.iloc[0][1])
    #             st.write(recommender_df.iloc[0][2])
    #             st.write(recommender_df.iloc[0][3])
    #             st.write(recommender_df.iloc[0][4])
    # else:
    #     st.write('Find our best sellers of Apple')


    # if "samsung" not in st.session_state:
    #     st.session_state["samsung"] = False

    # if st.button("Check Samsung's Products"):
    #     st.session_state["apple"] = False
    #     st.session_state["samsung"] = not st.session_state["samsung"]
    #     st.session_state["adidas"] = False
    #     st.session_state["chanel"] = False
    #     st.session_state["nintendo"] = False

    # if st.session_state['samsung'] == True:
    #     with st.form(key = 'edit_form_samsung'):
    #             # print is visible in the server output, not in the page

    #         product = ['Product_s1', 'Product_s2', 'Product_s3', 'Product_s4', 'Product_s5']
    #         recommender = ['r1','r2','r3','r4','r5'], ['r6','r7','r8','r9','r10'], ['r11','r12','r13','r14','r15'], ['r16','r17','r18','r19','r20'],['r21','r22','r23','r24','r25']
    #         df = get_select_box_data(product, recommender)
    #         option = st.selectbox('Select a product', df['Product'])

    #         if st.form_submit_button(label='Product Selected'):
    #             filtered_df = df[df['Product'] == option]
    #             recommender_df = filtered_df['Recommender']
    #             st.write('Recommender')
    #             st.write(recommender_df.iloc[0][0])
    #             st.write(recommender_df.iloc[0][1])
    #             st.write(recommender_df.iloc[0][2])
    #             st.write(recommender_df.iloc[0][3])
    #             st.write(recommender_df.iloc[0][4])
    # else:
    #     st.write('Find our best sellers of Samsung')


    # if "adidas" not in st.session_state:
    #     st.session_state["adidas"] = False

    # if st.button("Check adidas' Products"):
    #     st.session_state["apple"] = False
    #     st.session_state["samsung"] = False
    #     st.session_state["adidas"] = not st.session_state["adidas"]
    #     st.session_state["chanel"] = False
    #     st.session_state["nintendo"] = False

    # if st.session_state['adidas'] == True:
    #     with st.form(key = 'edit_form_adidas'):
    #             # print is visible in the server output, not in the page

    #         product = ['Product_a1', 'Product_a2', 'Product_a3', 'Product_a4', 'Product_a5']
    #         recommender = ['r1','r2','r3','r4','r5'], ['r6','r7','r8','r9','r10'], ['r11','r12','r13','r14','r15'], ['r16','r17','r18','r19','r20'],['r21','r22','r23','r24','r25']
    #         df = get_select_box_data(product, recommender)
    #         option = st.selectbox('Select a product', df['Product'])

    #         if st.form_submit_button(label='Product Selected'):
    #             filtered_df = df[df['Product'] == option]
    #             recommender_df = filtered_df['Recommender']
    #             st.write('Recommender')
    #             st.write(recommender_df.iloc[0][0])
    #             st.write(recommender_df.iloc[0][1])
    #             st.write(recommender_df.iloc[0][2])
    #             st.write(recommender_df.iloc[0][3])
    #             st.write(recommender_df.iloc[0][4])
    # else:
    #     st.write('Find our best sellers of adidas')


    # if "chanel" not in st.session_state:
    #     st.session_state["chanel"] = False

    # if st.button("Check Chanel's Products"):
    #     st.session_state["apple"] = False
    #     st.session_state["samsung"] = False
    #     st.session_state["adidas"] = False
    #     st.session_state["chanel"] = not st.session_state["chanel"]
    #     st.session_state["nintendo"] = False

    # if st.session_state['chanel'] == True:
    #     with st.form(key = 'edit_form_chanel'):
    #             # print is visible in the server output, not in the page

    #         product = ['Product1', 'Product2', 'Product3', 'Product4', 'Product5']
    #         recommender = ['r1','r2','r3','r4','r5'], ['r6','r7','r8','r9','r10'], ['r11','r12','r13','r14','r15'], ['r16','r17','r18','r19','r20'],['r21','r22','r23','r24','r25']
    #         df = get_select_box_data(product, recommender)
    #         option = st.selectbox('Select a product', df['Product'])

    #         if st.form_submit_button(label='Product Selected'):
    #             # st.session_state["FormSubmitter:edit_form-Product Selected"] = not st.session_state["FormSubmitter:edit_form-Product Selected"]
    #             filtered_df = df[df['Product'] == option]
    #             recommender_df = filtered_df['Recommender']
    #             st.write('Recommender')
    #             st.write(recommender_df.iloc[0][0])
    #             st.write(recommender_df.iloc[0][1])
    #             st.write(recommender_df.iloc[0][2])
    #             st.write(recommender_df.iloc[0][3])
    #             st.write(recommender_df.iloc[0][4])
    # else:
    #     st.write('Find our best sellers of Chanel')


#     if "nintendo" not in st.session_state:
#         st.session_state["nintendo"] = False

#     if st.button("Check Nintendo's Products"):
#         st.session_state["apple"] = False
#         st.session_state["samsung"] = False
#         st.session_state["adidas"] = False
#         st.session_state["chanel"] = False
#         st.session_state["nintendo"] = not st.session_state["nintendo"]

#     if st.session_state['nintendo'] == True:
#         with st.form(key = 'edit_form_nintendo'):
#             # print is visible in the server output, not in the page

#             product = ['Product1', 'Product2', 'Product3', 'Product4', 'Product5']
#             recommender = ['r1','r2','r3','r4','r5'], ['r6','r7','r8','r9','r10'], ['r11','r12','r13','r14','r15'], ['r16','r17','r18','r19','r20'],['r21','r22','r23','r24','r25']
#             df = get_select_box_data(product, recommender)
#             option = st.selectbox('Select a product', df['Product'])

#             if st.form_submit_button(label='Product Selected'):
#                 # st.session_state["FormSubmitter:edit_form-Product Selected"] = not st.session_state["FormSubmitter:edit_form-Product Selected"]
#                 filtered_df = df[df['Product'] == option]
#                 recommender_df = filtered_df['Recommender']
#                 st.write('Recommender')
#                 st.write(recommender_df.iloc[0][0])
#                 st.write(recommender_df.iloc[0][1])
#                 st.write(recommender_df.iloc[0][2])
#                 st.write(recommender_df.iloc[0][3])
#                 st.write(recommender_df.iloc[0][4])
#     else:
#         st.write('Find our best sellers of Nintendo')

# st.write(
#     f"""
#     ## Session state:
#     {st.session_state["apple"]=}

#     {st.session_state["samsung"]=}

#     {st.session_state["adidas"]=}

#     {st.session_state["chanel"]=}

#     {st.session_state["nintendo"]=}
#     {st.session_state}
#     """
# )
