import streamlit as st
import pandas as pd


st.title('Hello SnowFlake!')
st.header('this my first time using streamlit')
st.text('🍞Hello Bitchs!')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

st.dataframe(my_fruit_list)

