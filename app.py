import os
import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(page_title="Gemini AI Content Generator", layout="wide")

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

st.title("Gemini AI Content Generator")

# Sidebar for PDF Upload
st.sidebar.header("Document Upload")
uploaded_pdf = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"])

pdf_text = ""
if uploaded_pdf is not None:
    reader = PdfReader(uploaded_pdf)
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            pdf_text += extracted + "\n"
    st.sidebar.success(f"PDF uploaded successfully! ({len(reader.pages)} pages)")

# Main Prompt Input
prompt = st.text_input("Enter a prompt:")

# Output Section
if prompt:
    if not api_key:
        st.error("Please set your GEMINI_API_KEY in the .env file or environment variables.")
    else:
        try:
            with st.spinner("Generating content..."):
                # Combine prompt with PDF text if available
                full_prompt = prompt
                if pdf_text:
                    full_prompt = f"Context from uploaded PDF:\n{pdf_text}\n\nUser Prompt: {prompt}"

                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(full_prompt)
                st.write(response.text)
        except Exception as e:
            st.error(f"Error generating content: {e}")
else:
    st.write("Please enter a prompt to generate content.")
