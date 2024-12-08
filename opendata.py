import pandas as pd
import streamlit as st
import requests
res = requests.get('https://ped.uspto.gov/api/queries/cms/public/13111111')
data = res.json()
df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)