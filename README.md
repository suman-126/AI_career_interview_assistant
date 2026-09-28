# 🤖 AI Career & Interview Assistant

An AI-powered career and interview preparation assistant built using **Python, Streamlit, LangChain, FAISS, Hugging Face Embeddings, FlashRank, and Ollama**.

The application is designed to help students, freshers, and job seekers prepare for technical and HR interviews through question answering, interview practice, AI feedback, score tracking, and resume analysis.

---

## 📌 Project Overview

The **AI Career & Interview Assistant** is an interactive Streamlit application that combines interview preparation with an advanced **Retrieval-Augmented Generation (RAG)** pipeline.

The application provides a category-based interview knowledge base and uses retrieval techniques to find relevant information before generating an answer.

It includes:

- 💬 Interview Question Answering
- 🎤 Practice Interview Mode
- 🤖 AI-Powered Interview Feedback
- 📊 Interview Score Tracking
- 📄 Resume Analysis
- 🧠 Metadata Filtering
- 🔎 Multi-Query Retrieval
- 🔍 Direct Similarity Retrieval
- 🎯 Topic Matching
- ⚡ FlashRank Reranking
- 🤖 TinyLlama LLM Fallback

---

## 🎯 Project Objectives

- Help freshers prepare for interviews.
- Provide category-based interview preparation.
- Retrieve relevant information from an interview knowledge base.
- Implement practical RAG concepts.
- Improve retrieval using multiple retrieval and reranking techniques.
- Provide AI-powered interview feedback.
- Allow users to practice interview questions.
- Track interview attempts and scores.
- Analyze uploaded resumes for interview preparation.
- Demonstrate an end-to-end AI application using local LLM technology.

---

# 🚀 Features

## 💬 1. Ask Questions

Users can ask interview-related questions through the chat interface.

The application:

- Uses the selected interview category.
- Applies metadata filtering.
- Uses Multi-Query Retrieval.
- Performs direct similarity retrieval.
- Combines retrieved documents.
- Matches the question with the document topic.
- Uses FlashRank to rerank relevant documents.
- Returns the most relevant answer.
- Displays retrieved context and document metadata when applicable.

### Example

```text
What is a list in Python?

🎤 2. Practice Interview

The Practice Interview mode provides an interactive interview experience.

The application:

Selects an interview question.
Displays the question to the user.
Accepts the user's answer.
Evaluates the answer using the AI model.
Provides interview feedback.
Tracks questions attempted.
Tracks the score.
Allows the user to continue with another question.

📚 3. Interview Categories

The application currently supports:

🐍 Python
🤖 AI / Machine Learning
💼 HR Interview
📊 Data Science
🗄️ SQL

🤖 4. AI-Powered Interview Feedback

After submitting an interview answer, the AI provides feedback to help the user improve.

The feedback can include:

What was correct
What could be improved
A better sample answer

The goal is to provide simple and practical interview preparation feedback.

📊 5. Interview Score Tracking

The Practice Interview mode tracks:

Questions Attempted
Score

This gives users a simple way to monitor their interview practice.

📄 6. Resume Analysis

Users can upload their resume in:

PDF format
TXT format

The application processes the uploaded resume and can identify information such as:

Skills
Education
Projects
Training
Work Experience
Areas to Improve
Interview Preparation Topics

The analysis is based on the information available in the uploaded resume.

🧠 Advanced RAG Pipeline

The project implements an advanced RAG-style retrieval workflow.

🔄 RAG Pipeline
                         ┌───────────────────┐
                         │   User Question   │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │ Category Selection│
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │ Metadata Filtering│
                         └─────────┬─────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
                    ▼                             ▼
          ┌──────────────────┐          ┌──────────────────┐
          │ Multi-Query      │          │ Direct Similarity│
          │ Retrieval        │          │ Retrieval        │
          └────────┬─────────┘          └────────┬─────────┘
                   │                             │
                   └──────────────┬──────────────┘
                                  ▼
                         ┌───────────────────┐
                         │ Combine Documents │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │  Topic Matching   │
                         └─────────┬─────────┘
                                   │
                        ┌──────────┴──────────┐
                        │                     │
                   Match Found            No Match
                        │                     │
                        ▼                     ▼
              ┌─────────────────┐    ┌─────────────────┐
              │ FlashRank       │    │ TinyLlama       │
              │ Reranking       │    │ LLM Fallback    │
              └────────┬────────┘    └────────┬────────┘
                       │                      │
                       └──────────┬───────────┘
                                  ▼
                         ┌───────────────────┐
                         │   Final Answer    │
                         └───────────────────┘

🔍 RAG Components
1. Metadata Filtering

Each interview document contains metadata such as:

Category
Topic
Difficulty

The selected interview category is used during retrieval so that documents from unrelated categories are not unnecessarily considered.

2. Multi-Query Retrieval

MultiQueryRetriever generates alternative versions of the user's question.

This can improve retrieval when the wording of the user's question differs from the wording used in the knowledge base.

3. Direct Similarity Retrieval

The application also performs direct similarity search using FAISS.

This provides another retrieval path for finding semantically similar documents.

The retrieved results are combined before the relevance checks.

4. Topic Matching

After retrieval, the application checks whether the retrieved document topic matches the main topic contained in the user's question.

This additional validation helps reduce unrelated retrieval results.

5. FlashRank Reranking

Relevant candidate documents are passed to FlashRank.

FlashRank reranks the documents according to their relevance to the user's question.

The highest-ranked relevant document is selected for the final knowledge-base answer.

6. LLM Fallback

When a matching knowledge-base topic is not found, the application can use TinyLlama to generate a short general AI answer.

This gives the application a fallback response instead of forcing an unrelated knowledge-base document to answer the question.

🔄 Complete Project Workflow

The overall application workflow can be summarized as:

                         ┌──────────────────────┐
                         │        User          │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Streamlit Interface  │
                         └──────────┬───────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                  │
                 ▼                  ▼                  ▼
          Ask Questions     Practice Interview   Resume Analysis
                 │                  │                  │
                 ▼                  ▼                  ▼
          Advanced RAG       Question + Answer    Upload Resume
             Pipeline               │                  │
                 │                  ▼                  ▼
                 │            AI Evaluation      Resume Processing
                 │                  │                  │
                 ▼                  ▼                  ▼
           Final Answer       AI Feedback       Resume Analysis
                                    │
                                    ▼
                              Score Tracking

🛠️ Technologies Used
Technology	                      Purpose
Python	                Core programming language
Streamlit	                Interactive web application
LangChain	                LLM and RAG application framework
LangChain Classic	           Retrieval components
FAISS	                      Vector similarity search
Hugging Face Embeddings	   Text embedding generation
Sentence Transformers	   Embedding model
FlashRank	               Document reranking
Ollama	               Local LLM runtime
TinyLlama	               Local language model
PyPDF	                     PDF resume processing


Embedding Model
sentence-transformers/all-MiniLM-L6-v2

LLM
tinyllama:latest

📁 Project Structure
AI_career_interview_assistant/
│
├── myenv/
│
├── stream.py
├── interview_data.txt
├── requirements.txt
├── .gitignore
└── README.md


Important Files
stream.py
Contains the Streamlit interface, interview modes, RAG pipeline, practice interview logic, and resume analysis workflow.

interview_data.txt
Contains the interview knowledge-base information.

requirements.txt
Contains the Python dependencies required by the project.

.gitignore
Prevents files such as the virtual environment from being uploaded to GitHub.

myenv/ is excluded from GitHub using .gitignore.


⚙️ Installation & Setup
1. Clone the Repository
git clone YOUR_GITHUB_REPOSITORY_URL

Then open the project folder:
cd AI_career_interview_assistant

2. Create a Virtual Environment
python -m venv myenv

Activate it on Windows:
myenv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Install and Run Ollama
Make sure Ollama is installed and running.

Download the TinyLlama model:
ollama pull tinyllama

You can also verify the model with:
ollama run tinyllama:latest

5. Run the Streamlit Application
streamlit run stream.py


Streamlit will display a local URL in the terminal.

Open that URL in your browser to use the application.

💡 How to Use
💬 Ask Questions
Open the application.
Select Ask Questions.
Select an interview category.
Enter an interview question.
Press Enter.
Review the generated answer.
When available, expand Retrieved Context to inspect the retrieved document and metadata.


🎤 Practice Interview
Select Practice Interview.
Select an interview category.
Start the interview.
Read the generated question.
Enter your answer.
Submit the answer.
Review the AI feedback.
Check your score.
Continue to the next question.


📄 Resume Analysis
Scroll to Resume Analysis.
Upload a PDF or TXT resume.
Click Analyze Resume.
Review the extracted resume information.
Review the interview preparation topics.


📌 Example Questions
🐍 Python
What is a list in Python?
What is a tuple?
What is a dictionary?
What is a function?

🤖 AI / Machine Learning
What is Artificial Intelligence?
What is Machine Learning?

📊 Data Science
What is Data Science?
What is Pandas?

🗄️ SQL
What is SQL?
What is a Primary Key?
What is a Foreign Key?
What is the difference between WHERE and HAVING?

💼 HR Interview
Tell me about yourself.
What are your strengths?


🎯 Project Use Cases
This application can be useful for:

College students
Freshers
Job seekers
Technical interview preparation
HR interview preparation
Python interview preparation
AI/ML interview preparation
Data Science interview preparation
SQL interview preparation
Resume-based interview preparation


📚 Key Learning Outcomes
Through this project, I learned how to:

Build an interactive Streamlit application.
Work with LangChain.
Integrate Ollama with LangChain.
Use a local LLM.
Generate embeddings using Hugging Face.
Store and search embeddings using FAISS.
Implement metadata filtering.
Implement Multi-Query Retrieval.
Combine retrieval results.
Implement topic-based matching.
Use FlashRank for document reranking.
Build an advanced RAG-style retrieval pipeline.
Create an AI interview practice system.
Manage Streamlit session state.
Process PDF documents using PyPDF.
Build a resume analysis workflow.
Create an end-to-end AI application.

🔐 Data & Privacy
The project uses local components such as Ollama, TinyLlama, FAISS, and local document processing.

Uploaded resume information is processed by the application for analysis and is not intended to be stored in the project repository.

Users should avoid uploading documents containing information they do not want processed by an application.


🔮 Future Improvements
Possible future improvements include:

Add more interview categories.
Expand the interview knowledge base.
Improve interview scoring.
Add interview history.
Add downloadable interview reports.
Add voice-based interview practice.
Improve resume recommendations.
Add job-description matching.
Add more advanced interview analytics.
Deploy the application online.


⭐ Project Highlights
✅ Streamlit AI Application
✅ Interview Question Answering
✅ Practice Interview Mode
✅ AI-Powered Feedback
✅ Interview Score Tracking
✅ Resume Analysis
✅ Hugging Face Embeddings
✅ FAISS Vector Search
✅ Metadata Filtering
✅ Multi-Query Retrieval
✅ Direct Similarity Retrieval
✅ Topic Matching
✅ FlashRank Reranking
✅ TinyLlama + Ollama
✅ LLM Fallback


👩‍💻 Author
Suman

AI & Python Learner

This project was developed as a college and portfolio project to demonstrate practical skills in:

Python • AI • RAG • LangChain • Streamlit • FAISS • Embeddings • LLMs

📌 Project Summary

The AI Career & Interview Assistant combines interview preparation, an advanced RAG-style retrieval pipeline, AI-powered interview feedback, score tracking, and resume analysis into one interactive application.

It demonstrates how Python, Streamlit, LangChain, FAISS, Hugging Face Embeddings, FlashRank, Ollama, and TinyLlama can be combined to build a practical AI-powered career and interview preparation application.