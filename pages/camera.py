from PIL import Image
import streamlit as st
import io
import extra_streamlit_components as stx
import time
import sys
import database_manager
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from compostable import analyze_image

import asyncio
try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
def get_manager():
    return stx.CookieManager()

st.sidebar.page_link('pages/camera.py', label='Upload')
st.sidebar.page_link('pages/leaderboard.py', label='Leaderboard')
st.sidebar.page_link('pages/map.py', label='Map')
st.sidebar.page_link('pages/dashboard.py', label='Dashboard')

with open('style.css') as f:
	st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)

def runPrompt():
    st.spinner("Computing...")

st.title("Camera")

if "image" not in st.session_state:
    st.session_state.image = None

image = st.camera_input("Take a picture")

if image:
    st.session_state.image = image

if st.session_state.image:
    st.image(st.session_state.image, caption="Captured Image", use_container_width=True)
else:
    st.write("No image captured yet.")

if st.button("Confirm Picture"):
    if st.session_state.image:
        img = Image.open(st.session_state.image)
        img.save("captured.jpg")
        #st.success("Image saved as captured.jpg")

        with st.spinner("Analyzing image..."):
             result = analyze_image("captured.jpg")
             #st.markdown("### Here's What We Found:")
             st.markdown(result)
             compostable = st.session_state.get("compostable", "unknown")
             compostable = st.session_state.get("compostable", "unknown")
             manager = get_manager()
             if compostable == "yes":
                cookie_points = manager.get("gained_points")
                time.sleep(2)
                if cookie_points: 
                    st.error("You have already gained points in the last 5 minutes. Thanks for helping the environment!")
                else:
                    cookie = manager.get("user_email")
                    time.sleep(2)
                    client = database_manager.init_connection()
                    database_manager.add_score(client, str(cookie), 'userInfo')
                    manager.set("gained_points", "gained_points", max_age=300)
                    time.sleep(2)
                    compostable = "no"
                    st.success("Congrats! You gained 1 point. Go to leaderboard to see your score.")
                 
             
