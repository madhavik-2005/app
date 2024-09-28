import streamlit as st
import pytesseract
from PIL import Image
import os
import sys
import subprocess
import shutil

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return output.decode('utf-8'), error.decode('utf-8')

st.title("Hindi and English Text Extractor")

st.write("Tesseract Setup and Diagnostics:")

is_deployed = os.environ.get('STREAMLIT_CLOUD') == 'true'
st.write(f"Deployment environment detected: {is_deployed}")

if is_deployed:
    
    commands = [
        "sudo apt-get update",
        "sudo apt-get install -y tesseract-ocr",
        "sudo apt-get install -y tesseract-ocr-hin",
        "sudo apt-get install -y tesseract-ocr-eng"
    ]

    for cmd in commands:
        output, error = run_command(cmd)
        st.write(f"Command: {cmd}")
        st.write(f"Output: {output}")
        if error:
            st.write(f"Error: {error}")

    traineddata_url = "https://github.com/tesseract-ocr/tessdata/raw/main/hin.traineddata"
    download_cmd = f"sudo wget {traineddata_url} -O /usr/share/tesseract-ocr/4.00/tessdata/hin.traineddata"
    output, error = run_command(download_cmd)
    st.write(f"Downloading traineddata: {output}")
    if error:
        st.write(f"Error downloading traineddata: {error}")

tessdata_prefix = '/usr/share/tesseract-ocr/4.00/tessdata/'
os.environ['TESSDATA_PREFIX'] = tessdata_prefix
st.write(f"TESSDATA_PREFIX set to: {os.environ.get('TESSDATA_PREFIX')}")

tesseract_cmd = shutil.which('tesseract')
st.write(f"Tesseract command found at: {tesseract_cmd}")

if tesseract_cmd:
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

version, error = run_command("tesseract --version")
st.write(f"Tesseract version: {version}")
if error:
    st.write(f"Error checking version: {error}")

tessdata_output, error = run_command(f"ls -l {tessdata_prefix}")
st.write("Contents of tessdata directory:")
st.write(tessdata_output)
if error:
    st.write(f"Error listing tessdata: {error}")

hin_traineddata_path = os.path.join(tessdata_prefix, 'hin.traineddata')
st.write(f"hin.traineddata exists: {os.path.exists(hin_traineddata_path)}")

language = st.radio("Select language for extraction:", ('Hindi', 'English', 'Both'))

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    try:
        if language == 'Hindi':
            extracted_text = pytesseract.image_to_string(image, lang='hin')
        elif language == 'English':
            extracted_text = pytesseract.image_to_string(image, lang='eng')
        else:  
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
        st.error("If this is related to Tesseract, please check the setup information above.")