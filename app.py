import streamlit as st
import requests
from fpdf import FPDF
import json

# Define the API endpoint for Ollama
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# Function to generate text using Llama 3.2 via Ollama API
def generate_text(prompt):
    payload = {
        "model": "llama3.2",
        "prompt": prompt
         # Adjust context size if needed
    }
    response = requests.post(OLLAMA_API_URL, json=payload)
    response.raise_for_status()
    st.write(response)

    # Split response into individual JSON objects
    # json_objects = response.text.splitlines()
    # for obj in json_objects:
    #     try:
    #         data = json.loads(obj)
    #         # Process each JSON object as needed
    #         print(data)
    #     except json.JSONDecodeError as e:
    #         print(f"Failed to parse JSON object: {e}")

def extract_text(data):
    if 'dialogue' in data:
        return data['dialogue'].get('bot', '')
    elif 'outputText' in data:
        return data['outputText']
    elif 'message' in data:
        return data['message']
    else:
        return "Unknown format"


def create_pdf(text, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.output(filename)

st.title("Resume and Cover Letter Generator")
st.subheader("Personalize your documents based on job descriptions")

# Input fields
job_description = st.text_area("Job Description")
company_name = st.text_input("Company Name")
generate_button = st.button("Generate Documents")

if generate_button:
    # Generate resume and cover letter
    resume_prompt = f"Generate a resume for a job at {company_name} with the following description: {job_description}"
    cover_letter_prompt = f"Generate a cover letter for a job at {company_name} with the following description: {job_description}"
    
    try:
        resume_text = generate_text(resume_prompt)
        cover_letter_text = generate_text(cover_letter_prompt)
        
        # Create PDFs
        # create_pdf(resume_text, "resume.pdf")
        # create_pdf(cover_letter_text, "cover_letter.pdf")
        st.write(resume_text)
        
        st.success("Documents generated successfully!")
        
        with open("resume.pdf", "rb") as file:
            st.download_button(label="Download Resume", data=file, file_name="resume.pdf", mime="application/pdf")
        
        with open("cover_letter.pdf", "rb") as file:
            st.download_button(label="Download Cover Letter", data=file, file_name="cover_letter.pdf", mime="application/pdf")
    
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while generating documents: {e}")