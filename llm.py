import streamlit as st
import ollama
from PyPDF2 import PdfReader


st.title("Llama 3.2 Text Input Response Generator")

resume = st.file_uploader("Upload your resume here:")


userName = st.text_input("Enter your Name:")
companyName = st.text_input("Enter the Company Name here:")
jobDescription = st.text_area("Enter your Job Description here:")

def scoringMechanism(coverLetter, jobDescription):
    response = ollama.chat(
                model='llama3.2:3b',
                messages=[{
                    'role': 'user',
                    'content': f'''Please evaluate the following cover letter against the provided job description and calculate an ATS score only, do not display any other suggestions or text, only the final scores based on the following criteria. Calculate the average of all the scores in different criterias and get me a final score in percentage:

1. Keyword Matching:
   - Assess the presence and frequency of specific keywords and phrases from the job description in the resume.
   - Ensure keywords are contextually relevant.

2. Job Match Rate:
   - Measure how closely the resume aligns with the job description in terms of skills, qualifications, and experience.

3. Quantifiable Metrics:
   - Identify and evaluate any quantifiable achievements in the resume that demonstrate measurable impact.

4. Formatting and Readability:
   - Check for proper formatting to ensure the resume is easily parsed. Note any complex formatting that might cause parsing errors.

5. Consistency and Accuracy:
   - Verify consistent formatting and accurate information, such as correct dates and absence of spelling errors.

Cover Letter Text: {coverLetter}
Job Description: {jobDescription}

Output Format: {{
  "ats_score": 0,  // Example score
  "keyword_matching": {{
    "score": 0,
    
  }},
  "job_match_rate": {{
    "score": 0,
    
  }},
  "quantifiable_metrics": {{
    "score": 0,
    
  }},
  "formatting_readability": {{
    "score": 0,
    
  }},
  "consistency_accuracy": {{
    "score": 0,
    
  }}
}}'''
                }])['message']['content']
    st.write(response)

def extract_text_from_pdf(file):
        reader = PdfReader(file)
        extracted_text = ""
        for page in reader.pages:
            extracted_text += page.extract_text()
        return extracted_text

if resume is not None:
    text = extract_text_from_pdf(resume)
    # print(text)

    if st.button("Test Resume"):
        try:
            response = ollama.chat(
                model='llama3.2:3b',
                messages=[{
                    'role': 'user',
                    'content': f'''Please analyze the following resume text and extract the information into the specified categories. Provide the output in a structured format suitable for storing in variables:
Work Experience: List each job title, company name, all theroles and responsibilities listed in the bullet points and duration.
Skillset: List all relevant skills.
Education: List each degree, institution, and graduation year.
Projects: List each project title and a brief description.
Resume Text:{text} Output Format:{{
  "work_experience": [
    {{"job_title": "Software Engineer", "company": "Tech Corp", "Roles and Responsibilities": "Responsible for developing and maintaining the company's software products.", "duration": "Jan 2020 - Present"}},
    ...
  ],
  "skillset": ["Python", "Machine Learning", ...],
  "education": [
    {{"degree": "B.Sc. in Computer Science", "institution": "University of Example", "year": "2019"}},
    ...
  ],
  "projects": [
    {{"title": "AI Chatbot", "description": "Developed a chatbot using NLP techniques."}},
    ...
  ]
}}'''
                }])['message']['content']
            
            st.write("Response from Llama 3.2:")
            st.text(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")

if st.button("Generate Cover Letter"):
    
    if jobDescription:
        try:
            response = ollama.chat(
                model='llama3.2:3b',
                messages=[{
                    'role': 'user',
                    'content': f'{text}. Please generate an ATS-friendly cover letter with paragraphs and in a format that is easy to read based on the following resume data and job description, {jobDescription}. The cover letter should highlight my relevant work experience, skills, and achievements that align with the job requirements. Ensure the language is professional and tailored to the job description provided. Note add the company name {companyName} and {userName} wherever necessary, which would be the name of the person who is applying for the job in the cover letter.'
                }]
            )['message']['content']
            
            st.write("Response from Llama 3.2:")
            # st.write(response)
            scoringMechanism(response, jobDescription)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a job description to generate a response.")


