import streamlit as st
import pdfplumber
import json
import os
import smtplib
from email.message import EmailMessage
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# Initialize LLM
llm = GoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.7
)

# Extract text from PDF
def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text

# Prompt for Resume Screening
prompt = PromptTemplate(
    input_variables=["resume_text", "job_description"],
    template="""
    You are an expert resume screener. Extract key details from the following resume text:
    
    Resume:
    {resume_text}
    
    Compare it with the given job description:
    {job_description}
    
    Provide a structured JSON response with skills, experience, education, score, and missing skills.
    """
)

# Resume Screening Chain
resume_screener_chain = LLMChain(llm=llm, prompt=prompt)

def calculate_similarity(resume_text, job_desc):
    response = resume_screener_chain.invoke({"resume_text": resume_text, "job_description": job_desc})
    response_text = response.get("text", "{}")
    response_text = response_text.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        return {"score": 0, "missing_skills": []}

# Email Function (Updated with Debugging & Validation)
def is_valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$", email)

def send_email(to_email, subject, body):
    if not is_valid_email(to_email):
        print("❌ Invalid email format")
        return False
    
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = to_email
    
    try:
        print(f"📧 Sending email to {to_email}")  # Debugging
        print(f"📧 Using Email: {EMAIL_USER}")   # Debugging
        print(f"🔑 Password Present: {'Yes' if EMAIL_PASS else 'No'}")  # Debugging

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

        print("✅ Email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Email Error: {e}")  # Debugging
        return False

# Streamlit UI
st.title("📄 Resume Screening System")
st.write("Upload your resume and get an instant evaluation!")

name = st.text_input("Candidate Name")
email = st.text_input("Candidate Email")
resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if st.button("Submit"):
    if name and email and resume_file:
        resume_text = extract_text_from_pdf(resume_file)
        job_description = "Looking for a Python Developer with AI expertise."
        response_data = calculate_similarity(resume_text, job_description)
        match_score = response_data.get("score", 0)
        missing_skills = response_data.get("missing_skills", [])

        st.write(f"### Match Score: {match_score}")
        st.write(f"### Missing Skills: {', '.join(missing_skills) if missing_skills else 'None'}")

        if match_score > 80:
            decision = "Congratulations! You have been shortlisted for an interview."
            subject = "Interview Invitation"
        elif 50 <= match_score <= 79:
            decision = "You have been shortlisted for future opportunities."
            subject = "Shortlist Notification"
        else:
            decision = "Thank you for applying. Unfortunately, we have decided to move forward with other candidates."
            subject = "Rejection Email"

            # AI Feedback for Improvement
            feedback_prompt = f"Suggest skills to improve for this candidate based on missing skills: {missing_skills}"
            feedback_response = llm.invoke(feedback_prompt)
            feedback = feedback_response.get("text", "No feedback available.") if isinstance(feedback_response, dict) else feedback_response
            decision += f"\n\nAI Feedback for Improvement:\n{feedback}"

        st.write(f"### Decision: {decision}")

        if send_email(email, subject, decision):
            st.success(f"📧 Email sent to {email}")
        else:
            st.error("❌ Error sending email. Check credentials.")
    else:
        st.error("Please fill all fields and upload a resume!")
