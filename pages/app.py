import streamlit as st
import database_manager
import pandas as pd

if "user_logged_in" in st.context.cookies:
    if(st.context.cookies["user_logged_in"] == 'false'):
        st.info('Please Login from the Home page and try again.')
        st.stop()

st.set_page_config(
    page_title="App",
    page_icon="👋",
)

st.sidebar.page_link('pages/app.py', label='Home')
st.sidebar.page_link('pages/camera.py', label='Camera')
st.sidebar.page_link('pages/map.py', label='Map')
st.sidebar.page_link('pages/dashboard.py', label='Dashboard')

client = database_manager.init_connection()
for cookie in st.context.cookies:
    st.write(f"{cookie}: {st.context.cookies[cookie]}")
st.button("Add one to your score", on_click=database_manager.add_score, args=(client, st.context.cookies['user_id'], 'userInfo'))  # Add one to the user's score

data = database_manager.get_data(client, 'userInfo')  # Get data from the database
df = pd.DataFrame(data)
del df['_id']
df = df.sort_values(by='score', ascending=False)  # Sort by score
st.dataframe(df)  # Display data in a dataframe
