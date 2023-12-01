# import libraries
import streamlit as st
import pdfplumber
import os
import openai
import fitz  # PyMuPDF
import requests
from io import BytesIO
from PIL import Image

# Access the OpenAI API key from secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Logo setup
image_path = Image.open('logo.jpg')
st.image(image_path)

##########################################################################################################
# Sidebar FAQ

with st.sidebar:
    # About section
    st.markdown("# Meet Kelly - Your AI Powered Academic Advising Assistant")
    st.markdown(
        "This AI Assistant allows you to share your academic interests and career goals, and "
        "receive personalized recommendations for university curriculum and classes! "
    )

    # Divider
    st.markdown("---")

    # How to use section
    st.markdown(
        "## How does this work? \n"
        "Our AI assistant is integrated with the latest version of university curriculum, checksheets, and coursework to help students\n"
        "in quickly finding relevant and accurate insights to plan for their future. Please review your final plan with your academic advisor after! \n"
    )

    st.markdown("---")

    st.markdown(
        """
        If you encounter any issues or have feedback, please [contact us](mailto:support@joinadvisorai.com).
        """
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

# select the file path of curriculum dynamically
file_path = f"https://raw.githubusercontent.com/1arjunarora/ku-aiassistant/main/checksheets/{Selected_label}.pdf"

# Get user query input
user_query = st.text_input("Enter your query:", "As a freshman, what classes should I take? Or I am in my 3rd semester, what classes should I take?")

##########################################################################################################

def upload_pdf_and_retrieve_info(file_path, user_query):
    response = requests.get(file_path)

    if response.status_code == 200:
        pdf_content = BytesIO(response.content)
        with pdfplumber.open(pdf_content) as pdf:
            pdf_text = ""
            for page in pdf.pages:
                pdf_text += page.extract_text()
    
        # Set up a prompt with the extracted text
        prompt = f"Start by saying thank you for asking the question! Then act like an academic advisor at Kutztown University, be concise with your suggestions, and recommend courses in bullet format if students ask about classes to take for a given scenario. Please reference this link at end [Reference](https://www.kutztown.edu/academics/colleges-and-departments/business/department-of-business-administration/curriculum/checksheets.html), and retrieve information about course requirements from the following PDF:\n{pdf_text}\n\nUser Query:. In the end of the response about classes, provide a disclaimer that the final course list should be approved by your academic advisor to ensure university guidelines are met. If students ask about career paths for a major, provide only 3 to 4 recommendations with relevant information on key skills, job titles, and example job activities. Do not provide very long answers or paragraph format."
    
        # Combine prompt and user query
        input_text = f"{prompt} {user_query} "
    
        # Call OpenAI's API for completion
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can choose another engine if needed
            prompt=input_text,
            temperature=0.2,
            max_tokens=500,
            n=1
        )
    
        # Extract and return the model's response
        return response['choices'][0]['text']

##########################################################################################################
# Process file and user query when a button is clicked
if st.button("Ask University's AI Assistant"):

    # Call the function to retrieve information
    model_response = upload_pdf_and_retrieve_info(file_path, user_query)

    # Display the model's response
    st.subheader("AI Assistant's Response:")
    st.write(model_response)
