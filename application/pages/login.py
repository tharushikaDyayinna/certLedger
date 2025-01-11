import streamlit as st
from db.firebase_app import login
from dotenv import load_dotenv
import os

from streamlit_extras.switch_page_button import switch_page

from utils.streamlit_utils import displayPDF, hide_icons, hide_sidebar, remove_whitespaces
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()

import base64
# Function to encode image to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Path to the local image
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
# st.set_page_config(layout="wide", initial_sidebar_state="expanded")

load_dotenv()

st.markdown("""
    <style>
    .stApp {
        background-color: #f0f0f0; /* Light gray background */
    }
    </style>
""", unsafe_allow_html=True)


# Initialize session state for 'profile' if it doesn't exist
if 'profile' not in st.session_state:
    st.session_state['profile'] = None  # Default or None

# Form for email and password input
with st.form("login"):
    email = st.text_input("Enter your email")
    password = st.text_input("Enter your password", type="password")
    
   
    submit = st.form_submit_button("Login")

# If the profile is not "Institute", provide the option to register
if st.session_state.profile != "Institute":
    clicked_register = st.button("New user? Click here to register!")
    
    if clicked_register:
        switch_page("register")

if submit:
    # Check if the profile is "Institute" and authenticate accordingly
    if st.session_state.profile == "Institute":
        valid_email = os.getenv("institute_email")
        valid_pass = os.getenv("institute_password")
        
        if email == valid_email and password == valid_pass:
            switch_page("institute")
        else:
            st.error("Invalid credentials!")
    
    # login verifier
    else:
        result = login(email, password)
        
        if result == "success":
            st.success("Login successful!")
            
            # Redirect based on the user's profile
            if st.session_state.profile == "Verifier":
                switch_page("verifier")
            elif st.session_state.profile == "Student":
                switch_page("student")
            #else:
               # st.error("Unknown profile! Please try again.")
        
        #  log fails
        else:
            st.error("Invalid credentials!")
