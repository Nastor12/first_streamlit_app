import streamlit as st
import pandas as pd
import requests 
import snowflake.connector
from urllib.error import URLError


my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list= my_fruit_list.set_index('Fruit')

fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Apple','Cantaloupe'])

fruits_to_show = my_fruit_list.loc[fruits_selected]

st.dataframe(fruits_to_show)

st.header("Fruityvice Fruit Advice!")

def get_fruit_choice(this_fruit_choice):
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
#st.text(fruityvice_response.json())
       normalized_fruit= pd.json_normalize(fruityvice_response.json())
   return normalized_fruit
  
try:
   fruit_choice = st.text_input('What fruit would you like information about?')
   if not fruit_choice:
      st.error('Please select a fruit!')
   else:
       back_from_function= get_fruit_choice(fruit_choice)
       st.dataframe(back_from_function)
except URLError as e:
  st.error()

st.stop()
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
st.header("The fruit load list contains:")
st.dataframe(my_data_rows)
add_my_fruit = st.text_input('What fruit would you like to add?','banana')
st.write('Thanks for adding ', add_my_fruit)

my_cur.execute("insert into fruit_load_list values('from streamlit');")



