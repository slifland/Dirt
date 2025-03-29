import streamlit as st

if not st.session_state.logged_in:
    st.info('Please Login from the Home page and try again.')
    st.stop()

st.set_page_config(
    page_title="App",
    page_icon="👋",
)

st.sidebar.page_link('pages/app.py', label='Home')
st.sidebar.page_link('pages/camera.py', label='Camera')