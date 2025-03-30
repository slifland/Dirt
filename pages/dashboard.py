import streamlit as st
import database_manager
import pandas as pd
import plotly.express as px

with open('style.css') as f:
	st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)

client = database_manager.init_connection()

data = database_manager.get_data(client, 'userInfo')  # Get data from the database
data_list = list(data)

data_category = database_manager.get_data(client, 'compostedItems')  # Get data from the database
data_list_category = list(data_category)

for record in data_list:
        record['id'] = record['id']
        record['score'] = int(record['score'])

total_composted = 0
for record in data_list_category:
        record['_id'] = record['_id']
        record['count'] = int(record['count'])
        total_composted += record['count']

df = pd.DataFrame(data_list)
df_category = pd.DataFrame(data_list_category)

st.title("%s+ Items Composted" % total_composted)

if 'id' in df.columns and 'score' in df.columns:
        st.title("Distribution of Compost Scores")
        fig = px.bar(df, x='id', y='score', title='Data Visualization')
        fig.layout.paper_bgcolor='#C2B280'
        fig.layout.plot_bgcolor='#C2B280'
        st.plotly_chart(fig)
else:
   st.error("Columns 'id' and 'score' not found in the data.")

if '_id' in df_category.columns and 'count' in df_category.columns:
        st.title("Distribution of Compost Categories")
        fig_category = px.pie(df_category, values ='count', names='_id', title='Data Visualization')
        fig_category.layout.paper_bgcolor='#C2B280'
        st.plotly_chart(fig_category)
else:
   st.error("Columns '_id' and 'count' not found in the data.")
