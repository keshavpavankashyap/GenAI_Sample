# -*- coding: utf-8 -*-
"""Img_generation_sample.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Y4EIVmdDge8j7iu2JWOfXpSfLM-95ZF8
"""

import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from openai import OpenAI

# Streamlit UI for OpenAI API key input
api_key = st.text_input("Enter your OpenAI API Key:", type="password")

# Initialize OpenAI client using the API key
if api_key:
    client = OpenAI(api_key=api_key)

# Function to generate images using OpenAI's DALL-E 3 model
def generate_image_from_text(prompt):
    try:
        # Generate the image using client.images.generate
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,  # Number of images to generate
            size="1024x1024"  # Size of the image
        )

        # Extract the URL of the generated image
        image_url = response.data[0].url
        st.success(f"Generated Image URL: {image_url}")

        # Fetch the image from the URL
        image_response = requests.get(image_url)
        img = Image.open(BytesIO(image_response.content))

        # Display the generated image
        st.image(img, caption="Generated Image", use_column_width=True)

        # Save the image locally (optional)
        img.save("generated_image.png")
        st.write("Image saved as 'generated_image.png'")

    except Exception as e:
        st.error(f"Error generating image: {str(e)}")

# Streamlit UI layout
st.title("Text-to-Image Generator using OpenAI's DALL-E 3 designed by Keshav")

# Input box for text prompt
prompt = st.text_input("Enter a text prompt to generate an image:")

# Button to generate the image
if st.button("Generate Image") and api_key and prompt:
    generate_image_from_text(prompt)
