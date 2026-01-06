import os
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import google.generativeai as genai

# Load environment variables from .env
load_dotenv()

# Configure the Google API key
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Function to get response from the updated Gemini model
def get_gemini_response(input_text, image):
    model = genai.GenerativeModel("gemini-1.5-flash")  # correct model ID

    if input_text and image:
        response = model.generate_content([input_text, image])
    elif input_text:
        response = model.generate_content([input_text])
    elif image:
        response = model.generate_content([image])
    else:
        response = None

    return response.text if response else "No response available."

# Initialize Streamlit app
st.set_page_config(page_title="Gemini Image Demo")
st.header("Image Recognizer Application")

# Input text prompt
input_text = st.text_input("Input Prompt:", key="input")

# Image uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Submit button
submit = st.button("Tell me about the image")

# Generate and display the response if submit is clicked
if submit:
    if input_text or image:
        response = get_gemini_response(input_text, image)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please provide either an input prompt or an image.")
