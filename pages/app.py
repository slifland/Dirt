import streamlit as st
import database_manager
import pandas as pd
import asyncio
import extra_streamlit_components as stx


try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

if not 'authenticated' in st.session_state:
    st.stop()

st.set_page_config(
    page_title="App",
    page_icon="👋",
)

def get_manager():
    return stx.CookieManager()

st.sidebar.page_link('pages/app.py', label='Home')
st.sidebar.page_link('pages/camera.py', label='Camera')
st.sidebar.page_link('pages/map.py', label='Map')
st.sidebar.page_link('pages/dashboard.py', label='Dashboard')

client = database_manager.init_connection()

manager = get_manager()
cookie = manager.get("user_email")
if cookie is None:
    st.error("User email not found in cookies")
    st.stop()
else:
    st.button("Add one to your score", on_click=database_manager.add_score, args=(client, str(cookie), 'userInfo'))  # Add one to the user's score

data = database_manager.get_data(client, 'userInfo')  # Get data from the database
df = pd.DataFrame(data)
del df['_id']
df = df.sort_values(by='score', ascending=False)  # Sort by score
st.dataframe(df)  # Display data in a dataframe

