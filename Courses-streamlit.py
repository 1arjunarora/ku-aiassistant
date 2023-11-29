# import libraries
import streamlit as st
import pdfplumber
import os
import openai
from PIL import Image
import fitz  # PyMuPDF

# Set your OpenAI API key
openai.api_key = "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"

# Logo setup
image_path = Image.open('logo.jpg')
st.image(image_path)

##########################################################################################################
# Sidebar FAQ

with st.sidebar:
    # About section
    st.markdown("# Meet Kelly - Your AI Academic Advisor")
    st.markdown(
        "This AI Assistant allows you to share your academic interests and career goals, and "
        "receive personalized recommendations for academic major, job potential, and classes! "
    )

    # Divider
    st.markdown("---")

    # How to use section
    st.markdown(
        "## How does this work? \n"
        "Our AI assistant is integrated with the latest version of university curriculum, checksheets, and coursework to help students\n"
        "in quickly finding relevant and accurate insights to plan for their future. Please review your final plan with your academic advisor after! \n"
    )

##########################################################################################################
# main app section setup
# List of options
options = [
    "Accounting",
    "Finance",
    "Entrepreneurship",
    "General Business",
    "Human Resource Management",
    "Personal Financial Planning",
    "Management",
    "Marketing",
    "Supply Chain Management",
    "Sports Management"
]

# User inputs
Selected_label = st.selectbox("Enter Your Preferred Major:", options)

# seleect the file path of curriculum dynamically
file_path = f"https://raw.githubusercontent.com/1arjunarora/ku-aiassistant/main/checksheets/{Selected_label}.pdf"

# Get user query input
user_query = st.text_input("Enter your query:", "As a freshman, what classes should I take? I am in my 3rd semester, what classes should I take?")

##########################################################################################################

def upload_pdf_and_retrieve_info(url, user_query):
    # Read the PDF file and extract text content
    with fitz.open(url) as pdf:
        pdf_text = ""
        for page_number in range(pdf.page_count):
            page = pdf[page_number]
            pdf_text += page.get_text()

    # Set up a prompt with the extracted text
    prompt = f"Act like an academic advisor at a university, be concise with your suggestions, and share your answers in bullet format. Additionally, answer the question asked by student, by starting with saying thank you for asking the question and mention that Students should meet with their advisors each semester to monitor their progress towards graduation requirements. Lastly, retrieve information from the following PDF:\n{pdf_text}\n\nUser Query:"

    # Combine prompt and user query
    input_text = f"{prompt} {user_query} "

    # Call OpenAI's API for completion
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can choose another engine if needed
        prompt=input_text,
        temperature=0.2,
        max_tokens=800,
        n=1
    )

    # Extract and return the model's response
    return response['choices'][0]['text']

# Process file and user query when a button is clicked
if st.button("Ask University's AI Assistant"):

    # Call the function to retrieve information
    model_response = upload_pdf_and_retrieve_info(file_path, user_query)

    # Display the model's response
    st.subheader("AI Assistant's Response:")
    st.write(model_response)
