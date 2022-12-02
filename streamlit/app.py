import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="eCommerce Rercommender", # => The title
    page_icon="🛒",
    layout="wide", # wide
    initial_sidebar_state="auto") # collapsed

st.title("Let's go shopping!")

col1, col2,col3, col4, col5 = st.columns(5)

with col1:
    image = Image.open('data/apple.png')
    st.image(image, caption='Apple')

    if "apple" not in st.session_state:
        st.session_state["apple"] = False

    if st.button("Check Apple's Products"):
        st.session_state["apple"] = not st.session_state["apple"]
        st.session_state["samsung"] = False
        if sum(st.session_state.values()) == 1:
            brand = [i for i in st.session_state if st.session_state[i]==True][0]
            with st.form(key = 'edit_form'):
                # print is visible in the server output, not in the page
                @st.cache
                def get_select_box_data():
                    # Remember to filter by brand here
                    return pd.DataFrame({
                    'Product': ['Product1', 'Product2', 'Product3', 'Product4', 'Product5'],
                    'Recommender': [['s1','s2','s3','s4','s5'], ['s6','s7','s8','s9','s10'], ['s11','s12','s13','s14','s15'], ['s16','s17','s18','s19','s20'],['s21','s22','s23','s24','s25']]
                    })

                df = get_select_box_data()
                option = st.selectbox('Select a product', df['Product'])

                if st.form_submit_button(label='Product Selected'):

                    filtered_df = df[df['Product'] == option]
                    # filtered_df = filtered_df[['Recommender']]

                    st.write('Recommender')
                    st.write(filtered_df.iloc[0, 2][0])
                    st.write(filtered_df.iloc[0, 2][1])
                    st.write(filtered_df.iloc[0, 2][2])
                    st.write(filtered_df.iloc[0, 2][3])
                    st.write(filtered_df.iloc[0, 2][4])
    else:
        st.write('Find our best sellers of Apple')

    if sum(st.session_state.values()) == 1:
        brand = [i for i in st.session_state if st.session_state[i]==True][0]
        with st.form(key = 'edit_form'):
            # print is visible in the server output, not in the page
            @st.cache
            def get_select_box_data():
                # Remember to filter by brand here
                return pd.DataFrame({
                'Product': ['Product1', 'Product2', 'Product3', 'Product4', 'Product5'],
                'Recommender': [['s1','s2','s3','s4','s5'], ['s6','s7','s8','s9','s10'], ['s11','s12','s13','s14','s15'], ['s16','s17','s18','s19','s20'],['s21','s22','s23','s24','s25']]
                })

            df = get_select_box_data()
            option = st.selectbox('Select a product', df['Product'])

            if st.form_submit_button(label='Product Selected'):

                filtered_df = df[df['Product'] == option]
                # filtered_df = filtered_df[['Recommender']]

                st.write('Recommender')
                st.write(filtered_df.iloc[0, 2][0])
                st.write(filtered_df.iloc[0, 2][1])
                st.write(filtered_df.iloc[0, 2][2])
                st.write(filtered_df.iloc[0, 2][3])
                st.write(filtered_df.iloc[0, 2][4])


with col2:
    image = Image.open('data/samsung.png')
    st.image(image, caption='Samsung')

    if "samsung" not in st.session_state:
        st.session_state["samsung"] = False

    if st.button("Check Samsung's Products"):
        st.session_state["samsung"] = not st.session_state["samsung"]
        st.session_state["apple"] = False

with col3:
    image = Image.open('data/adidas.png')
    st.image(image, caption='adidas')

    if st.button("Check adidas' Products"):
        st.session_state["samsung"] = not st.session_state["samsung"]
        st.session_state["apple"] = False

with col4:
    image = Image.open('data/chanel.png')
    st.image(image, caption='Chanel')

    if st.button("Check Chanel' Products"):
        st.session_state["samsung"] = not st.session_state["samsung"]
        st.session_state["apple"] = False

with col5:
    image = Image.open('data/nintendo.png')
    st.image(image, caption='Nintendo')

    if st.button("Check Nintendo' Products"):
        st.session_state["samsung"] = not st.session_state["samsung"]
        st.session_state["apple"] = False
# if "apple" not in st.session_state:
#     st.session_state["apple"] = False

# if "samsung" not in st.session_state:
#     st.session_state["samsung"] = False

# if st.button("Check Apple's Products"):
#     st.session_state["apple"] = not st.session_state["apple"]
#     st.session_state["samsung"] = False



# if st.button("Check Samsung's Products"):
#     st.session_state["samsung"] = not st.session_state["samsung"]
#     st.session_state["apple"] = False

# if sum(st.session_state.values()) == 1:
#     brand = [i for i in st.session_state if st.session_state[i]==True][0]
#     with st.form(key = 'edit_form'):
#         # print is visible in the server output, not in the page
#         @st.cache
#         def get_select_box_data():
#             # Remember to filter by brand here
#             return pd.DataFrame({
#             'Product': ['Product1', 'Product2', 'Product3', 'Product4', 'Product5'],
#             'Recommender': [['s1','s2','s3','s4','s5'], ['s6','s7','s8','s9','s10'], ['s11','s12','s13','s14','s15'], ['s16','s17','s18','s19','s20'],['s21','s22','s23','s24','s25']]
#             })

#         df = get_select_box_data()
#         option = st.selectbox('Select a product', df['Product'])

#         if st.form_submit_button(label='Product Selected'):

#             filtered_df = df[df['Product'] == option]
#             filtered_df = filtered_df[['Recommender']]

#             st.write('Recommender')
#             st.write(filtered_df.iloc[0, 0][0])
#             st.write(filtered_df.iloc[0, 0][1])
#             st.write(filtered_df.iloc[0, 0][2])
#             st.write(filtered_df.iloc[0, 0][3])
#             st.write(filtered_df.iloc[0, 0][4])
# else:
#     st.write('Find our best sellers of Apple')
