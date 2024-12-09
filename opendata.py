import pandas as pd
import streamlit as st
import requests

id:list = ['17021772','17205017','17475162']
data:list = []

for i in id:
    res = requests.get(f'https://ped.uspto.gov/api/queries/cms/public/{i}')
    if res.status_code == 200:
        json = res.json()
        data.append(json[0])
    else:
        print(f'回傳錯誤的id:{i}')

df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)