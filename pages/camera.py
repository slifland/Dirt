import streamlit as st

with open('style.css') as f:
	st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)

def runPrompt():
	st.text("Computing")

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
    runPrompt()
