import streamlit as st
from db.firebase_app import register
from streamlit_extras.switch_page_button import switch_page
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces
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

# Add custom CSS for background color
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f0f0; /* Light gray background */
    }
    </style>
""", unsafe_allow_html=True)

# Clear the sidebar
st.sidebar.empty()

# Create the registration form
form = st.form("login")
email = form.text_input("Enter your email")
password = form.text_input("Enter your password", type="password")
clicked_login = st.button("Already registered? Click here to login!")

# Redirect to the login page if the login button is clicked
if clicked_login:
    switch_page("login")

submit = form.form_submit_button("Register")
if submit:
    # Register the user using email and password
    result = register(email, password)
    
    # If registration is successful
    if result == "success":
        st.success("Registration successful!")
        
        # Redirect based on the user's profile
        if st.session_state.profile == "Institute":
            switch_page("institute")
        elif st.session_state.profile == "Verifier":
            switch_page("verifier")
        elif st.session_state.profile == "Student":  # Add this check for student profile
            switch_page("student")  # Redirect to student page
        else:
            st.error("Unknown profile! Please try again.")
    
    # If registration fails
    else:
        st.error("Registration unsuccessful!")
