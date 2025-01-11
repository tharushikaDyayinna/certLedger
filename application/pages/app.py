import streamlit as st
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces
from streamlit_extras.switch_page_button import switch_page
import base64


st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()


def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


image_path = "../assets/rm222batch2-mind-03.jpg"
encoded_image = get_base64_image(image_path)

# Add CSS to set the background image using base64 encoding
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
""", unsafe_allow_html=True)

# Add custom CSS for background color
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f0f0; /* Light gray background */
    }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin: 10px;
        width: 90%;
    }
    .card-title {
        font-size: 24px;
        margin-bottom: 10px;
    }
    .card-button {
        padding: 10px 20px;
        border-radius: 5px;
        background-color: #4CAF50;
        color: white;
        border: none;
        cursor: pointer;
        font-size: 16px;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Creating columns for cards
col1, col2 = st.columns(2)

# Card for Institute
with col1:
    st.markdown("""
        <div class="card">
            <h3 class="card-title">Institute</h3>
            <p>Generate and manage certificates for verification process.</p>
        </div>
    """, unsafe_allow_html=True)
    clicked_institute = st.button("Enter", key="institute_button", help="Go to Institute Login")

# Card for Verifier
with col2:
    st.markdown("""
        <div class="card">
            <h3 class="card-title">Verifier</h3>
            <p>Verify certificates submitted by candidates or institutions.</p>
        </div>
    """, unsafe_allow_html=True)
    clicked_verifier = st.button("Enter", key="verifier_button", help="Go to Verifier Login")

# Handle button clicks inside the cards
if clicked_institute:
    st.session_state.profile = "Institute"
    switch_page('login')
elif clicked_verifier:
    st.session_state.profile = "Verifier"
    switch_page('login')
