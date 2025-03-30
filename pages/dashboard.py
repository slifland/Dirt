import streamlit as st
import database_manager
import pandas as pd
import plotly.express as px

client = database_manager.init_connection()

data = database_manager.get_data(client, 'userInfo')  # Get data from the database
data_list = list(data)

for record in data_list:
        record['id'] = record['id']
        record['score'] = int(record['score'])

df = pd.DataFrame(data_list)

if 'id' in df.columns and 'score' in df.columns:
   st.title("MongoDB Data with Plotly")
   fig = px.bar(df, x='id', y='score', title='Data Visualization')
   st.plotly_chart(fig)
else:
   st.error("Columns 'field1' and 'field2' not found in the data.")

