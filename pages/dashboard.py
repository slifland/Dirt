import streamlit as st
import database_manager
import pandas as pd
import plotly.express as px

client = database_manager.init_connection()

data = database_manager.get_data(client, 'accounts')  # Get data from the database
data_list = list(data)

for record in data_list:
        record['account_id'] = int(record['account-id']['$numberInt'])
        record['limit'] = int(record['limit']['$numberInt'])

df = pd.DataFrame(data_list)

st.write(df.head())

fig = px.bar(df, x='field1', y='field2', title='Data Visualization')

st.title("MongoDB Data with Plotly")
st.plotly_chart(fig)
