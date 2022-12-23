import streamlit as st
import pandas as pd
import requests 

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list= my_fruit_list.set_index('Fruit')

fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Apple','Cantaloupe'])

fruits_to_show = my_fruit_list.loc[fruits_selected]

st.dataframe(fruits_to_show)

st.header("Fruityvice Fruit Advice!")

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response.json())

normalized_fruit= pd.json_normalize(fruityvice_response.json())
st.dataframe(normalized_fruit)

