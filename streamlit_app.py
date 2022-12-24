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

st.header("The fruit load list contains:")

def get_fruit_load_list():
   with my_cnx.cursor() as my_cur:
      my_cur.execute("select * from fruit_load_list")
      return my_cur.fetchall()
   

if st.button('Get fruit List!'):
   my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
   my_data_rows=get_fruit_load_list()
   my_cnx.close()
   st.dataframe(my_data_rows)

def insert_row_snowflake(new_fruit):
   with my_cnx.cursor() as my_cur:
      my_cur.execute("insert into fruit_load_list values('"+ new_fruit +"')")
      return "Thanks for adding " + new_fruit
   
add_my_fruit = st.text_input('What fruit would you like to add?')

if st.button('Adding a new fruit!'):
   my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
   new_added_fruit= insert_row_snowflake(add_my_fruit)
   my_cnx.close()
   st.dataframe(new_added_fruit)
   

st.text('Thanks for adding ' + add_my_fruit)


