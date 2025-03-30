import streamlit as st
import database_manager
import pandas as pd
import asyncio
import extra_streamlit_components as stx
import matplotlib
import time


try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

st.set_page_config(
    page_title="Leaderboard",
    page_icon="👋",
)

def get_manager():
    return stx.CookieManager()

st.sidebar.page_link('pages/camera.py', label='Upload Image')
st.sidebar.page_link('pages/leaderboard.py', label='Leaderboard')
st.sidebar.page_link('pages/map.py', label='Map')
st.sidebar.page_link('pages/dashboard.py', label='Dashboard')

client = database_manager.init_connection()

manager = get_manager()
cookie = manager.get("user_email")
time.sleep(2)
if cookie is None:
    st.error("User email not found in cookies")
    st.stop()
else:
    st.button("Add one to your score", on_click=database_manager.add_score, args=(client, str(cookie), 'userInfo'))  # Add one to the user's score

compostable = st.session_state.get("compostable", "unknown")
if compostable == "yes":
    cookie = manager.get("gained_points", None)
    if cookie: 
        st.error("You have already gained points in the last 5 minutes. Try again soon.")
    else:
        database_manager.add_score(client, str(cookie), 'userInfo')
        manager.set("gained_points", "gained_points", max_age=300)
        time.sleep(2)
        compostable = "no"

data = database_manager.get_data(client, 'userInfo')  # Get data from the database
df = pd.DataFrame(data)
del df['_id']
df = df.sort_values(by='score', ascending=False).reset_index(drop=True)  # Sort by score
# Assign Medals to the Email Column
medals = ["🥇", "🥈", "🥉"]
df["id"] = df["id"].astype(str)  # Ensure it's a string column
df.loc[:2, "id"] = [medals[i] + " " + email for i, email in enumerate(df["id"][:3])]

st.title("🏆 Leaderboard 🏆")

styled_df = df.style.background_gradient(subset='score', cmap='RdYlGn')

st.dataframe(styled_df, hide_index=True, use_container_width=True)

