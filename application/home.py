import streamlit as st
from PIL import Image
from streamlit_extras.switch_page_button import switch_page
import base64
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces
# Hide the sidebar
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
hide_icons()
hide_sidebar()
remove_whitespaces()


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


# Custom 3D Text Effect with Centered Title
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800&display=swap');

    /* Set the background color for the entire app */
    .stApp {
        background-color: #f0f0f0; /* Light gray background */
    }

    .custom-3d-text {
        font-family: 'Montserrat', sans-serif;
        font-size: 40px; 
        font-weight: 800;
        color: #000; 
        position: relative;
        display: inline-block;
        padding: 30px; 
        margin: 0;
        line-height: 1.5; 
        letter-spacing: 1px;
        text-shadow: 
            2px 2px 0px #FFF, /* White shadow */
            3px 3px 0px rgba(0, 0, 0, 0.5); /* Black shadow for depth */
    }

    .centered {
        text-align: center; /* Center align the text */
    }

    .subtitle {
        font-size: 18px;
        color: gray;
        text-align: center;
        margin-top: 5px; /* Adjust as needed */
    }
    </style>

    <div class="centered">
        <h1 class="custom-3d-text"> 
            Effortlessly Certify, Verify, and Authenticate
        </h1>
    </div>
    """, unsafe_allow_html=True)

# Subtitle or additional text
st.markdown("""
<p class="subtitle">
    Protect your credentials with the security of blockchain technology.
</p>
""", unsafe_allow_html=True)


#st.markdown("<h1>Effortlessly certify, verify, and authenticate documents</h1>", unsafe_allow_html=True)
#st.markdown("<p>Secure your credentials with blockchain technology.</p>", unsafe_allow_html=True)



image = Image.open('../assets/0.jpg')  
#resized_image = image.resize((500, 500))
#st.image(resized_image, caption=None)
#st.image(image, caption=None, use_column_width=50)
# Create columns to center the image
col1, col2, col3 = st.columns([1, 2, 1])  # Adjust column widths if necessary
with col2:
    st.image(image, use_column_width=True)  # Display image in the center column
# Create an empty container for the button to position it
button_container = st.empty()  # Create an empty container

# Display the 'Get Started' button in the top right corner
with button_container.container():  # Use the container context
    st.markdown('<div style="text-align: right;">', unsafe_allow_html=True)  # Align to right
    if st.button("Get Started"):
        switch_page('app')  # This will take the user to the next page
    st.markdown('</div>', unsafe_allow_html=True)  # Close the div
