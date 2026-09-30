# 🤖 AI Career & Interview Assistant

An AI-powered career and interview preparation assistant built using **Python, Streamlit, LangChain, FAISS, Hugging Face Embeddings, FlashRank, and Ollama**.

The application is designed to help students, freshers, and job seekers prepare for technical and HR interviews through question answering, interview practice, practice tests, score tracking, progress monitoring, and resume analysis.
---

## 📌 Project Overview

The **AI Career & Interview Assistant** is an interactive Streamlit application that combines interview preparation with an advanced **Retrieval-Augmented Generation (RAG)** pipeline.

The application provides a category-based interview knowledge base and uses multiple retrieval techniques to find relevant information before generating an answer.

It includes:
* 💬 Interview Question Answering
* 🎤 Practice Interview Mode
* 📝 Practice Test Mode
* 🤖 AI-Powered Interview Feedback
* 📊 Interview Score Tracking
* 📈 Progress Dashboard
* 📄 Resume Analysis
* 🎯 Difficulty-Based Questions
* 🧠 Metadata Filtering
* 🔎 Multi-Query Retrieval
* 🔍 Direct Similarity Retrieval
* 🎯 Topic Matching
* ⚡ FlashRank Reranking
* 🤖 TinyLlama LLM Fallback
* 🔄 Practice Test Retake
---

## 🎯 Project Objectives

* Help students and freshers prepare for interviews.
* Provide category-based interview preparation.
* Provide different difficulty levels for interview questions.
* Retrieve relevant information from an interview knowledge base.
* Implement practical RAG concepts.
* Improve retrieval using multiple retrieval and reranking techniques.
* Provide interview practice functionality.
* Provide AI-powered interview feedback.
* Provide practice tests with scoring.
* Track interview and test performance.
* Provide a progress dashboard.
* Analyze uploaded resumes for interview preparation.
* Demonstrate an end-to-end AI application using local LLM technology.
---

# 🚀 Features

## 💬 1. Ask Questions
Users can ask interview-related questions through the chat interface.

The application:
* Uses the selected interview category.
* Applies metadata filtering.
* Uses Multi-Query Retrieval.
* Performs direct similarity retrieval.
* Combines retrieved documents.
* Matches the question with the document topic.
* Uses FlashRank to rerank relevant documents.
* Returns the most relevant knowledge-base answer.
* Displays retrieved context and document metadata when applicable.
* Uses TinyLlama as a general AI fallback when a matching knowledge-base topic is not found.

### Example
```text
What is a list in Python?
```
---

## 🎤 2. Practice Interview
The Practice Interview mode provides an interactive interview experience.

The application:
* Selects an interview question.
* Displays the question to the user.
* Accepts the user's answer.
* Evaluates the submitted answer.
* Provides interview feedback.
* Tracks questions attempted.
* Tracks the interview score.
* Classifies the answer as correct, partially correct, or incorrect.
* Allows the user to continue with another question.

The Practice Interview feature helps users simulate interview-style question answering and improve their responses.
---

## 📝 3. Practice Test
The Practice Test mode allows users to test their interview knowledge through a short quiz.

The application:
* Generates a practice test with up to 5 questions.
* Uses the selected interview category.
* Uses the selected difficulty level.
* Accepts the user's answers.
* Evaluates each answer.
* Classifies answers as:

  * Correct
  * Partially Correct
  * Incorrect
* Calculates the total score.
* Displays the test percentage.
* Shows detailed results for each question.
* Allows the user to retake the test.

The Practice Test feature helps users check their knowledge and identify topics that require additional preparation.
---

## 📚 4. Interview Categories
The application currently supports:

* 🐍 Python
* 🤖 AI / Machine Learning
* 💼 HR Interview
* 📊 Data Science
* 🗄️ SQL

Each category contains interview questions organized by topic and difficulty.
---

## 🎯 5. Difficulty Levels
The application supports three difficulty levels:

* 🟢 Beginner
* 🟡 Intermediate
* 🔴 Advanced

Difficulty information is stored as metadata with the interview knowledge-base documents.

This allows users to practice questions according to their current preparation level.
---

## 🤖 6. AI-Powered Interview Feedback
After submitting an interview answer, the application provides feedback to help the user improve.

The feedback can include:
* What was correct.
* What could be improved.
* A better sample answer.
* A brief explanation of the expected answer.

The current answer evaluation uses the application's answer-matching and scoring logic.

Advanced semantic LLM-based answer evaluation can be added as a future improvement.
---

## 📊 7. Interview Score Tracking
The Practice Interview mode tracks:

* Questions Attempted
* Correct Answers
* Interview Score

This provides users with a simple way to monitor their interview practice.
---

## 📈 8. Progress Dashboard
The Progress Dashboard provides an overview of the user's interview preparation progress.

### 📝 Practice Test Progress
The dashboard tracks:

* Tests Completed
* Questions Attempted
* Total Score
* Correct Answers
* Partially Correct Answers
* Incorrect Answers

### 🎤 Practice Interview Progress
The dashboard tracks:

* Questions Attempted
* Correct Answers
* Interview Score

The dashboard provides a simple overview of practice performance and helps users monitor their preparation.
---

## 📄 9. Resume Analysis
Users can upload their resume in:

* PDF format
* TXT format

The application processes the uploaded resume and can identify information such as:

* Skills
* Education
* Projects
* Training
* Work Experience
* Strengths
* Areas to Improve
* Recommended Interview Categories
* Interview Preparation Topics
* Fresher-related information

The analysis is based on the information available in the uploaded resume.

---

# 🧠 Advanced RAG Pipeline
The project implements an advanced RAG-style retrieval workflow.

## 🔄 RAG Pipeline

```text
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
                ┌─────────────┴─────────────┐
                │                           │
                ▼                           ▼
      ┌──────────────────┐        ┌──────────────────┐
      │ Multi-Query      │        │ Direct Similarity│
      │ Retrieval        │        │ Retrieval        │
      └────────┬─────────┘        └────────┬─────────┘
               │                           │
               └─────────────┬─────────────┘
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
                   │                     │
                   └──────────┬──────────┘
                              ▼
                    ┌───────────────────┐
                    │   Final Answer    │
                    └───────────────────┘
```
---

## 🔍 RAG Components

### 1. Metadata Filtering
Each interview document contains metadata such as:

* Category
* Topic
* Difficulty

The selected interview category is used during retrieval so that documents from unrelated categories are not unnecessarily considered.
---

### 2. Multi-Query Retrieval
The application uses `MultiQueryRetriever`.

It generates alternative versions of the user's question to improve retrieval when the wording of the user's question differs from the wording used in the knowledge base.
---

### 3. Direct Similarity Retrieval
The application also performs direct similarity search using FAISS.

This provides another retrieval path for finding semantically similar documents.

The retrieved results from the different retrieval paths are combined before further relevance checks.
---

### 4. Topic Matching
After retrieval, the application checks whether the retrieved document topic matches the main topic contained in the user's question.

This additional validation helps reduce unrelated retrieval results.
---

### 5. FlashRank Reranking
Relevant candidate documents are passed to FlashRank.

FlashRank reranks the retrieved documents according to their relevance to the user's question.

The highest-ranked relevant document is selected for the final knowledge-base answer.
---

### 6. LLM Fallback
When a matching knowledge-base topic is not found, the application can use TinyLlama to generate a short general AI answer.

This provides a fallback response instead of forcing an unrelated knowledge-base document to answer the question.
---

# 🔄 Complete Project Workflow

```text
                         ┌──────────────────────┐
                         │        User          │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Streamlit Interface  │
                         └──────────┬───────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
       Ask Questions        Practice Interview      Practice Test
              │                     │                     │
              ▼                     ▼                     ▼
        Advanced RAG          Question + Answer      Test Questions
          Pipeline                   │                     │
              │                      ▼                     ▼
              │                Answer Evaluation     Test Evaluation
              │                      │                     │
              ▼                      ▼                     ▼
        Final Answer            AI Feedback          Test Results
                                    │                     │
                                    └──────────┬──────────┘
                                               │
                                               ▼
                                      Progress Dashboard


                         ┌──────────────────────┐
                         │   Resume Analysis    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                            Upload Resume
                                    │
                                    ▼
                           Resume Processing
                                    │
                                    ▼
                            Resume Analysis
```

---

# 🛠️ Technologies Used

| Technology              | Purpose                           |
| ----------------------- | --------------------------------- |
| Python                  | Core programming language         |
| Streamlit               | Interactive web application       |
| LangChain               | LLM and RAG application framework |
| LangChain Classic       | Retrieval components              |
| LangChain Community     | FAISS and related integrations    |
| FAISS                   | Vector similarity search          |
| Hugging Face Embeddings | Text embedding generation         |
| Sentence Transformers   | Embedding model                   |
| FlashRank               | Document reranking                |
| Ollama                  | Local LLM runtime                 |
| TinyLlama               | Local language model              |
| PyPDF                   | PDF resume processing             |

### Embedding Model
```text
sentence-transformers/all-MiniLM-L6-v2
```

### LLM
```text
tinyllama:latest
```
---

# 📁 Project Structure

```text
AI_career_interview_assistant/
│
├── myenv/
│
├── stream.py
├── interview_data.txt
├── requirements.txt
├── .gitignore
└── README.md
```
---

# 📁 Important Files

### `stream.py`
Contains the Streamlit interface, interview modes, RAG pipeline, practice interview logic, practice test system, progress dashboard, and resume analysis workflow.

### `interview_data.txt`
Contains the interview knowledge-base information, including categories, topics, questions, answers, and difficulty levels.

### `requirements.txt`
Contains the Python dependencies required by the project.

### `.gitignore`
Prevents files such as the virtual environment and other unnecessary files from being uploaded to GitHub.

`myenv/` is excluded from GitHub using `.gitignore`.
---

# ⚙️ Installation & Setup

## 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Then open the project folder:

```bash
cd AI_career_interview_assistant
```
---

## 2. Create a Virtual Environment

```bash
python -m venv myenv
```

Activate it on Windows:

```bash
myenv\Scripts\activate
```
---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```
---

## 4. Install and Run Ollama
Make sure Ollama is installed and running.

Download the TinyLlama model:

```bash
ollama pull tinyllama
```

You can also verify the model with:

```bash
ollama run tinyllama:latest
```
---

## 5. Run the Streamlit Application
```bash
streamlit run stream.py
```

Streamlit will display a local URL in the terminal.
Open that URL in your browser to use the application.
---

# 💡 How to Use

## 💬 Ask Questions
1. Open the application.
2. Select **Ask Questions**.
3. Select an interview category.
4. Select a difficulty level if applicable.
5. Enter an interview question.
6. Press Enter.
7. Review the generated answer.
8. When available, expand **Retrieved Context** to inspect the retrieved document and metadata.
---

## 🎤 Practice Interview
1. Select **Practice Interview**.
2. Select an interview category.
3. Select a difficulty level.
4. Start the interview.
5. Read the generated question.
6. Enter your answer.
7. Submit the answer.
8. Review the feedback.
9. Check your score.
10. Continue to the next question.
---

## 📝 Practice Test
1. Select **Practice Test**.
2. Select an interview category.
3. Select a difficulty level.
4. Start the practice test.
5. Answer the displayed questions.
6. Submit the test.
7. Review the score and percentage.
8. Review correct, partially correct, and incorrect answers.
9. Use **Retake Test** to practice again.
---

## 📈 Progress Dashboard
1. Open the **Progress Dashboard** from the sidebar.
2. Review Practice Test statistics.
3. Review Practice Interview statistics.
4. Check questions attempted and scores.
5. Use the progress information to identify areas that need additional practice.
---

## 📄 Resume Analysis
1. Open the Resume Analysis section.
2. Upload a PDF or TXT resume.
3. Click **Analyze Resume**.
4. Review the extracted resume information.
5. Review detected skills, projects, education, training, and other information.
6. Review the recommended interview preparation topics.
---

# 📌 Example Questions

## 🐍 Python
* What is a list in Python?
* What is a tuple?
* What is a dictionary?
* What is a function?
* What is a decorator?
* What is a generator?

## 🤖 AI / Machine Learning
* What is Artificial Intelligence?
* What is Machine Learning?
* What is supervised learning?
* What is classification?
* What is overfitting?
* What is a neural network?

## 📊 Data Science
* What is Data Science?
* What is Pandas?
* What is correlation?
* What is an outlier?
* What is PCA?

## 🗄️ SQL
* What is SQL?
* What is a Primary Key?
* What is a Foreign Key?
* What is the difference between WHERE and HAVING?
* What is an INNER JOIN?
* What is a GROUP BY clause?

## 💼 HR Interview
* Tell me about yourself.
* What are your strengths?
* What is your weakness?
* Why should we hire you?
* How do you handle criticism?
* How do you handle pressure?
---

# 🎯 Project Use Cases
This application can be useful for:

* College students
* Freshers
* Job seekers
* Technical interview preparation
* HR interview preparation
* Python interview preparation
* AI/ML interview preparation
* Data Science interview preparation
* SQL interview preparation
* Resume preparation
* Interview practice
* Knowledge testing
* Interview progress tracking
---

# 📚 Key Learning Outcomes
Through this project, I learned how to:

* Build an interactive Streamlit application.
* Work with LangChain.
* Integrate Ollama with LangChain.
* Use a local LLM.
* Generate embeddings using Hugging Face.
* Store and search embeddings using FAISS.
* Implement metadata filtering.
* Implement Multi-Query Retrieval.
* Combine retrieval results.
* Implement topic-based matching.
* Use FlashRank for document reranking.
* Build an advanced RAG-style retrieval pipeline.
* Create an AI interview practice system.
* Build a practice test system.
* Implement test scoring.
* Classify answers as correct, partially correct, or incorrect.
* Manage Streamlit session state.
* Track interview and test progress.
* Build a progress dashboard.
* Implement difficulty-based question selection.
* Create a retake workflow.
* Process PDF documents using PyPDF.
* Build a resume analysis workflow.
* Create an end-to-end AI application.
---

# 🔐 Data & Privacy

* The project uses local components such as Ollama, TinyLlama, FAISS, and local document processing.
* Uploaded resume information is processed by the application for analysis.
* Resume files are not intended to be stored in the project repository.
* Users should avoid uploading documents containing information they do not want processed by an application.
* The project should be configured appropriately before being deployed publicly.
---

# 🔮 Future Improvements
Possible future improvements include:

* Add more interview categories.
* Expand the interview knowledge base.
* Improve interview scoring.
* Replace rule-based answer evaluation with advanced LLM-based semantic evaluation.
* Add personalized interview questions based on uploaded resumes.
* Add persistent interview and test history using SQLite.
* Add downloadable interview reports.
* Add advanced mock interview sessions.
* Add detailed performance analytics.
* Add voice-based interview practice.
* Improve resume recommendations.
* Add job-description matching.
* Deploy the application online.

These features are planned as possible future enhancements and are not part of the current completed version.
---

# ⭐ Project Highlights

✅ Streamlit AI Application
✅ Interview Question Answering
✅ Practice Interview Mode
✅ Practice Test Mode
✅ AI-Powered Interview Feedback
✅ Interview Score Tracking
✅ Progress Dashboard
✅ Difficulty-Based Questions
✅ Practice Test Scoring
✅ Correct / Partial / Incorrect Evaluation
✅ Practice Test Retake
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
✅ Advanced RAG Pipeline

---

# 👩‍💻 Author

**Suman**

AI & Python Learner
Passionate about building practical applications using:
**Python • AI • RAG • LangChain • Streamlit • FAISS • Embeddings • LLMs**
---

# 📌 Project Summary

The **AI Career & Interview Assistant** combines interview preparation, an advanced RAG-style retrieval pipeline, interview practice, practice testing, scoring, progress tracking, and resume analysis into one interactive application.

It demonstrates how **Python, Streamlit, LangChain, FAISS, Hugging Face Embeddings, FlashRank, Ollama, and TinyLlama** can be combined to build a practical AI-powered career and interview preparation application.
