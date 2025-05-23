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

st.sidebar.page_link('pages/camera.py', label='Upload')
st.sidebar.page_link('pages/leaderboard.py', label='Leaderboard')
st.sidebar.page_link('pages/map.py', label='Map')
st.sidebar.page_link('pages/dashboard.py', label='Dashboard')

with open('style.css') as f:
	st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)

def runPrompt():
    st.spinner("Computing...")

st.title("dirt")
st.title("Compostable?")
st.title("Take a Picture!")

if "image" not in st.session_state:
    st.session_state.image = None
        

image = st.camera_input("")

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
        with st.spinner("Analyzing image..."):
            result = analyze_image("captured.jpg")
            st.markdown(result)
            compostable = st.session_state.get("compostable", "unknown")
            if compostable == "yes":
                if database_manager.add_score(None, st.session_state.get("user_email"), "userInfo"):
                    st.success("Congrats! You gained 1 point. Go to leaderboard to see your score.")
                else:
                    st.error("You can't earn points because it has been less than 5 minutes since your last point. Thanks for helping to saving the environment!")
                st.session_state['compostable'] = 'no'

                # if st.button("Go to leaderboard"):
                #     st.switch_page('pages/leaderboard.py')
             
#test