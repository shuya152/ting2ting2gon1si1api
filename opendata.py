import streamlit as st
import requests
res = requests.get('https://ped.uspto.gov/api/queries/cms/public/13111111')
data = res.json()
st.table(data)