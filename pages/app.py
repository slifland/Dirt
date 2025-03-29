import streamlit as st
import database_manager
import pandas as pd

if not st.session_state.logged_in:
    st.info('Please Login from the Home page and try again.')
    st.stop()

st.set_page_config(
    page_title="App",
    page_icon="👋",
)

st.sidebar.page_link('pages/app.py', label='Home')
st.sidebar.page_link('pages/camera.py', label='Camera')

client = database_manager.init_connection()

st.button("Add One", on_click=database_manager.add_score, args=(client, '10', 'userInfo'))  # Add one to the score
data = database_manager.get_data(client, 'userInfo')  # Get data from the database
df = pd.DataFrame(data)
del df['_id']
df = df.sort_values(by='score', ascending=False)  # Sort by score
st.dataframe(df)  # Display data in a dataframe