from PIL import Image
import streamlit as st
import io

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from compostable import analyze_image

st.sidebar.page_link('pages/app.py', label='Home')
st.sidebar.page_link('pages/camera.py', label='Camera')
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
        st.success("Image saved as captured.jpg")

        with st.spinner("Analyzing image..."):
             result = analyze_image("captured.jpg")
             st.markdown("### Here's What We Found:")
             st.markdown(result)
