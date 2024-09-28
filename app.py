import streamlit as st
import pytesseract
from PIL import Image
import os
import sys

if os.environ.get('STREAMLIT_CLOUD') == 'true':
   
    os.system('sudo apt-get update')
    os.system('sudo apt-get install -y tesseract-ocr')
    os.system('sudo apt-get install -y tesseract-ocr-hin')
   
    pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
else:
   
    pass

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("Hindi and English Text Extractor")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    try:
        extracted_text = pytesseract.image_to_string(image, lang='hin+eng')
        
        st.subheader("Extracted Text:")
        st.text(extracted_text)
        
        keyword = st.text_input("Enter a keyword to search within the extracted text:")
        
        if keyword:
            if keyword in extracted_text:
                highlighted_text = extracted_text.replace(
                    keyword, f"<span style='color: red; font-weight: bold;'>{keyword}</span>"
                )
                st.subheader("Search Results:")
                st.markdown(highlighted_text.replace("\n", "  \n"), unsafe_allow_html=True)
            else:
                st.write("Keyword not found.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("If this is related to Tesseract, please ensure it's properly installed on the server.")