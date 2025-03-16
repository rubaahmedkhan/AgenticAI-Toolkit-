# 📄 Resume Screening System

## 🚀 Overview
The **Resume Screening System** is an AI-powered tool that evaluates resumes against job descriptions. It utilizes **LangChain, Gemini AI, and Streamlit** to extract key details from resumes and assess candidates' qualifications.

## 🔥 Features
- 📄 **PDF Resume Parsing**: Extracts text from uploaded resumes.
- 🤖 **AI-Powered Screening**: Uses Google Gemini (via LangChain) to compare resumes with job descriptions.
- 🎯 **Match Score Calculation**: Determines candidate suitability based on extracted skills and experience.
- ✉️ **Automated Email Notifications**: Notifies candidates with interview results and AI-generated feedback.
- 🖥️ **Streamlit UI**: Provides an interactive web interface for resume submission.

## 🌍 Live Demo
The project is deployed on Hugging Face Spaces. Try it here:  
🔗 **[Resume Screening System](https://huggingface.co/spaces/RubaKhan242/resume)**

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/AgenticAI-Toolkit.git
   cd AgenticAI-Toolkit
   ```
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables (`.env` file):
   ```
   GEMINI_API_KEY=your_google_api_key
   EMAIL_USER=your_email@example.com
   EMAIL_PASS=your_email_password
   ```

## 🚀 Usage

Run the application using:
```bash
streamlit run app.py
```

### User Flow
1. Enter your **name** and **email**.
2. Upload your **resume (PDF format)**.
3. The system extracts resume details and compares them with a predefined job description.
4. Candidates receive a **match score** and **missing skills** analysis.
5. If selected, an **automated email** is sent with interview details or feedback.

## 📧 Email Notifications
- **Interview Invitation** (Score > 80)
- **Shortlist Notification** (Score between 50-79)
- **Rejection Email** with AI-generated improvement suggestions (Score < 50)

## 🏗️ Future Improvements
- 🔍 **Custom Job Descriptions**: Allow users to input their own job descriptions.
- 📊 **Dashboard for Recruiters**: Visualize candidate analytics.
- 🌍 **Multi-Language Support**: Enhance compatibility with non-English resumes.

## 🤝 Contributing
Feel free to fork this repository and submit a pull request with improvements! 🚀
