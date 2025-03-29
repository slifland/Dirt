import streamlit as st

st.title("Camera Input")

image = st.camera_input("Compost?")

if image:
	st.image(image, caption="Captured Image", use_column_width = True)
else:
	st.write("No image captured yet.")
