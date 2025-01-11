import streamlit as st
import os
import hashlib
from utils.cert_utils import extract_certificate
from utils.streamlit_utils import displayPDF, view_certificate
from PIL import Image 
from connection import contract
from streamlit_extras.switch_page_button import switch_page
from utils.streamlit_utils import displayPDF
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


st.sidebar.markdown("") 

# Add custom CSS for background color
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f0f0; /* Light gray background */
    }
    </style>
""", unsafe_allow_html=True)

# Title for the verification page
st.markdown("<h1 style='text-align: center;'>Verify Certificate</h1>", unsafe_allow_html=True)

# Welcome message
st.markdown("<h4 style='text-align: center;'>Welcome to the Verifier Portal! Easily verify and view certificates with just a few clicks.</h4>", unsafe_allow_html=True)

# Options for certificate verification
options = ("Verify Certificate using PDF", "View/Verify Certificate using Certificate ID")
selected = st.selectbox("", options, label_visibility="hidden")

st.write("")  # Adds space

if selected == options[0]:
    uploaded_file = st.file_uploader("Upload the PDF version of the certificate")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        with open("certificate.pdf", "wb") as file:
            file.write(bytes_data)
        try:
            (uid, candidate_name, course_name, org_name) = extract_certificate("certificate.pdf")
            displayPDF("certificate.pdf")
            os.remove("certificate.pdf")

            # Calculating hash
            data_to_hash = f"{uid}{candidate_name}{course_name}{org_name}".encode('utf-8')
            certificate_id = hashlib.sha256(data_to_hash).hexdigest()

            # Smart Contract Call
            result = contract.functions.isVerified(certificate_id).call()
            if result:
                st.success("Certificate verified successfully!")
            else:
                st.error("Invalid Certificate! Certificate might be tampered")
        except Exception as e:
            st.error("Invalid Certificate! Certificate might be tampered")

elif selected == options[1]:
    form = st.form("Validate-Certificate")
    certificate_id = form.text_input("Enter the Certificate ID")
    submit = form.form_submit_button("Verify")
    if submit:
        try:
            view_certificate(certificate_id)
            # Smart Contract Call
            result = contract.functions.isVerified(certificate_id).call()
            if result:
                st.success("Certificate verified successfully!")
            else:
                st.error("Invalid Certificate ID!")
        except Exception as e:
            st.error("Invalid Certificate ID!")
