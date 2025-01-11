import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
import hashlib
from utils.cert_utils import generate_certificate
from utils.streamlit_utils import view_certificate
from connection import contract, w3
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




# Load environment variables
load_dotenv()
api_key = os.getenv("PINATA_API_KEY")
api_secret = os.getenv("PINATA_API_SECRET")

# Function to upload files to Pinata
def upload_to_pinata(file_path, api_key, api_secret):
    # Set up the Pinata API endpoint and headers
    pinata_api_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": api_key,
        "pinata_secret_api_key": api_secret,
    }

    # Prepare the file for upload
    with open(file_path, "rb") as file:
        files = {"file": (file.name, file)}

        # Make the request to Pinata
        response = requests.post(pinata_api_url, headers=headers, files=files)

        # Parse the response
        result = json.loads(response.text)

        if "IpfsHash" in result:
            ipfs_hash = result["IpfsHash"]
            print(f"File uploaded to Pinata. IPFS Hash: {ipfs_hash}")
            return ipfs_hash
        else:
            print(f"Error uploading to Pinata: {result.get('error', 'Unknown error')}")
            return None

# Add custom CSS for background color
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f0f0; /* Light gray background */
    }
    </style>
""", unsafe_allow_html=True)

# Title for the issue certificate page
st.markdown("<h1 style='text-align: center;'>Issue Certificate</h1>", unsafe_allow_html=True)

# Welcome message
st.markdown("<h4 style='text-align: center;'>Welcome to the Institute Portal! Seamlessly manage and issue certificates with confidence.</h4>", unsafe_allow_html=True)

# Options for certificate management
options = ("Generate Certificate", "View Certificates")
selected = st.selectbox("", options, label_visibility="hidden")

if selected == options[0]:
    form = st.form("Generate-Certificate")
    uid = form.text_input(label="University ID")
    candidate_name = form.text_input(label="Name of the Student")
    course_name = form.text_input(label="Course Name")
    org_name = form.text_input(label="University")

    submit = form.form_submit_button("Submit")
    if submit:
        pdf_file_path = "certificate.pdf"
        institute_logo_path = "../assets/images.png"
        generate_certificate(pdf_file_path, uid, candidate_name, course_name, org_name, institute_logo_path)

        # Upload the PDF to Pinata
        ipfs_hash = upload_to_pinata(pdf_file_path, api_key, api_secret)
        os.remove(pdf_file_path)
        data_to_hash = f"{uid}{candidate_name}{course_name}{org_name}".encode('utf-8')
        certificate_id = hashlib.sha256(data_to_hash).hexdigest()

        # Smart Contract Call
        contract.functions.generateCertificate(certificate_id, uid, candidate_name, course_name, org_name, ipfs_hash).transact({'from': w3.eth.accounts[0]})
        st.success(f"Certificate successfully generated with Certificate ID: {certificate_id}")

else:
    form = st.form("View-Certificate")
    certificate_id = form.text_input("Enter the Certificate ID")
    submit = form.form_submit_button("Submit")
    if submit:
        try:
            view_certificate(certificate_id)
        except Exception as e:
            st.error("Invalid Certificate ID!")
