import streamlit as st

# Set a custom background color for the whole page
st.markdown(
    """
    <style>
    div.stAppViewContainer.appview-container.st-emotion-cache-1yiq2ps.eht7o1d0 {
        background-color: #C2B280;
        color: #3E2723;
        text-align: center;
    }
    header.stAppHeader.st-emotion-cache-12fmjuu.e4hpqof0{
        background-color: #7B9A50;
        color: 7C4D28#;
    }
    video{
        background-color: #7B9A50;
        color: 7C4D28#;
    }
    button.st-emotion-cache-khjqke.e47j7ja9{
        background-color: #7B9A50;
        color: 7C4D28#;
    }
    button.st-emotion-cache-khjqke.e47j7ja9:hover{
        background-color: #FFD700;
        color: 7C4D28#;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title of the app
st.title("Camera")

# Add a camera input widget
image = st.camera_input("")

# If an image is captured, display it
if image:
    st.image(image, caption="Captured Image", use_column_width=True)
else:
    st.write("No image captured yet.")
