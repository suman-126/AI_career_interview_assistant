# 🤖 AI Career & Interview Assistant

An AI-powered career and interview preparation assistant built using Python, Streamlit, LangChain, FAISS, Hugging Face Embeddings, and Ollama.

The application helps freshers prepare for interviews, practice interview questions, receive AI-powered feedback, and analyze their resumes.


## 📌 Project Overview

The **AI Career & Interview Assistant** is an interactive Streamlit application designed to help students and freshers prepare for technical and HR interviews.

The application provides interview questions from a knowledge base and uses a vector database to retrieve relevant answers. It also provides a Practice Interview mode where users can answer questions and receive AI-generated feedback.

The application also includes a Resume Analysis feature that extracts useful information such as skills, education, projects, training, and work experience from an uploaded resume.


## 🎯 Project Objectives

- Help freshers prepare for interviews.
- Provide category-based interview questions.
- Retrieve relevant answers from an interview knowledge base.
- Provide AI-powered interview feedback.
- Allow users to practice interview questions.
- Track interview attempts and scores.
- Analyze resumes for interview preparation.
- Provide general AI assistance when a question is not available in the knowledge base.


## 🚀 Features

### 💬 1. Ask Questions
Users can ask interview-related questions through the chat interface.

The application:
- Searches the interview knowledge base.
- Uses FAISS for similarity search.
- Filters questions according to the selected category.
- Returns the relevant answer.
- Uses Ollama for general AI answers when the question is not found in the knowledge base.

### 🎤 2. Practice Interview

Users can practice interviews by selecting a category and starting an interview.

The application:
- Selects an interview question randomly.
- Displays the question to the user.
- Allows the user to submit their answer.
- Evaluates the answer using an AI model.
- Provides interview feedback.
- Shows questions attempted.
- Tracks the user's score.
- Allows the user to move to the next question.


### 📚 3. Interview Categories

The application provides four interview categories:

- Python
- AI / Machine Learning
- HR Interview
- Data Science

### 🤖 4. AI-Powered Feedback

After submitting an interview answer, the AI provides:

- What was correct
- What could be improved
- A better sample answer

The feedback is designed to be simple and useful for interview preparation.

### 📊 5. Interview Score Tracking

The Practice Interview mode tracks:

- Questions Attempted
- Score

This helps users monitor their interview practice.


### 📄 6. Resume Analysis

Users can upload their resume in:

- PDF format
- TXT format

The application analyzes the resume and identifies:
- Skills
- Education
- Projects
- Training
- Work Experience
- Areas to Improve
- Interview Preparation Topics

The resume analysis is based only on the information available in the uploaded resume.


## 🧹 Data Processing

The interview questions and answers are stored in:`interview_data.txt`

The application processes the file and separates the content into different interview categories.

Each question and its answer are converted into documents with category metadata.

This allows FAISS to retrieve relevant questions based on the selected interview category.

## 🔍 Vector Search

The project uses **Hugging Face Sentence Transformers** to create embeddings.

Embedding model used:

`sentence-transformers/all-MiniLM-L6-v2`

These embeddings are stored in a **FAISS vector store**.

FAISS is used to find the most relevant interview question based on the user's query.

## 🧠 AI Model

The project uses **Ollama** with the:

`tinyllama:latest`

model.

Ollama is used for:

- General AI answers
- Interview answer evaluation
- Resume analysis
- AI-powered interview feedback


## 🛠️ Technologies Used

- Python
- Streamlit
- LangChain
- FAISS
- Hugging Face Embeddings
- Sentence Transformers
- Ollama
- TinyLlama
- PyPDF


## 📁 Project Structure

```text
AI_career_interview_assistant/
│
├── myenv/
│
├── stream.py
│
├── interview_data.txt
│
└── README.md

▶️ How to Run the Project
1. Open the project folder
Open the project in VS Code.

2. Activate the virtual environment
Activate the myenv virtual environment.

3. Run the Streamlit application
streamlit run stream.py

4. Open the application
Streamlit will provide a local URL in the terminal.

Open that URL in your browser.

💡 How to Use
○ Ask Questions
- Select Ask Questions.
- Select an interview category.
- Enter your interview question.
- Press Enter.

The application retrieves the relevant answer or provides a general AI answer.

○ Practice Interview
- Select Practice Interview.
- Select an interview category.
- Click Start Interview.
- Read the interview question.
- Enter your answer.
- Click Submit Answer.
- Read the AI feedback.
- Click Next Question to continue practicing.

○ Resume Analysis
- Scroll to Resume Analysis.
- Upload a PDF or TXT resume.
- Click Analyze Resume.
- Review the extracted skills, education, projects, training, experience, and interview preparation topics.

🎯 Project Use Cases
This project can be useful for:

- College students 
- Freshers
- Job seekers
- Technical interview preparation
- HR interview preparation
- Python interview preparation
- Data Science interview preparation
- AI/ML interview preparation
- Resume-based interview preparation

📌 Key Learning Outcomes
Through this project, I learned how to:

- Build an interactive Streamlit application.
- Work with LangChain.
- Use Ollama with LangChain.
- Generate embeddings using Hugging Face.
- Store and search embeddings using FAISS.
- Build a basic RAG-style question-answering system.
- Create an AI interview practice system.
- Maintain Streamlit session state.
- Process PDF resumes using PyPDF.
- Build a resume analysis workflow.
- Create an end-to-end AI application.


🔮 Future Improvements
Some possible future improvements include:

- Add more interview categories.
- Add more questions to the knowledge base.
- Improve interview scoring.
- Add voice-based interview practice.
- Add interview history.
- Add downloadable interview reports.
- Add more advanced resume recommendations.
- Deploy the application online.


👩‍💻 Author
- Suman

⭐ Project Summary

The AI Career & Interview Assistant combines interview preparation, vector search, AI feedback, and resume analysis into one application.

It demonstrates how Python, LangChain, FAISS, Hugging Face Embeddings, Ollama, and Streamlit can be combined to build a practical AI-powered career assistance application.