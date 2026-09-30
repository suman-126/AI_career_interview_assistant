# IMPORTS
import streamlit as st
import random
from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langchain_community.document_compressors import FlashrankRerank
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

# CHAT HISTORY

if "messages" not in st.session_state:
    st.session_state.messages = []

# PRACTICE INTERVIEW STATE

if "practice_started" not in st.session_state:
    st.session_state.practice_started = False

if "practice_question" not in st.session_state:
    st.session_state.practice_question = None  

if "practice_answer_key" not in st.session_state:
    st.session_state.practice_answer_key = None

if "practice_feedback" not in st.session_state:
    st.session_state.practice_feedback = None

if "practice_attempted" not in st.session_state:
    st.session_state.practice_attempted = 0

if "practice_score" not in st.session_state:
    st.session_state.practice_score = 0

if "last_submitted_question" not in st.session_state:
    st.session_state.last_submitted_question = None

# PRACTICE TEST STATE

if "test_started" not in st.session_state:
    st.session_state.test_started = False

if "test_questions" not in st.session_state:
    st.session_state.test_questions = []

if "test_answers" not in st.session_state:
    st.session_state.test_answers = {}

if "test_submitted" not in st.session_state:
    st.session_state.test_submitted = False

if "test_score" not in st.session_state:
    st.session_state.test_score = 0

if "test_results" not in st.session_state:
    st.session_state.test_results = []

if "test_id" not in st.session_state:
    st.session_state.test_id = 0    

# PROGRESS DASHBOARD STATE
if "show_dashboard" not in st.session_state:
    st.session_state.show_dashboard = False

if "tests_completed" not in st.session_state:
    st.session_state.tests_completed = 0

if "total_test_questions" not in st.session_state:
    st.session_state.total_test_questions = 0

if "total_correct_answers" not in st.session_state:
    st.session_state.total_correct_answers = 0

if "total_partial_answers" not in st.session_state:
    st.session_state.total_partial_answers = 0

if "total_incorrect_answers" not in st.session_state:
    st.session_state.total_incorrect_answers = 0

if "total_test_score" not in st.session_state:
    st.session_state.total_test_score = 0

if "interview_questions_attempted" not in st.session_state:
    st.session_state.interview_questions_attempted = 0

if "interview_correct_answers" not in st.session_state:
    st.session_state.interview_correct_answers = 0

if "interview_score" not in st.session_state:
    st.session_state.interview_score = 0

#IMPORT THE MODEL OF CHAT OLLAMA

llm = ChatOllama(
    model="tinyllama:latest",
    temperature=0,
    num_predict=500
)

# ---------------------------------------------------------
# TITLE & CUSTOM CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 40px;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 8px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 28px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# MAIN TITLE
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">🤖 AI Career & Interview Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your AI-powered interview preparation assistant</div>',
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.header("🤖 AI Interview Assistant")

    st.write(
        "Prepare for your interviews with "
        "AI-powered assistance."
    )

    st.divider()

    # -----------------------------------------------------
    # KNOWLEDGE BASE
    # -----------------------------------------------------

    st.subheader("📚 Knowledge Base")

    st.write("Interview Data")

    # -----------------------------------------------------
    # FEATURES
    # -----------------------------------------------------

    st.subheader("⚡ Features")

    st.write("• Interview Questions")
    st.write("• AI-powered Answers")
    st.write("• Document-based Answers")
    st.write("• Practice Interview")
    st.write("• Practice Test")
    st.write("• Resume Analysis")

    # -----------------------------------------------------
    # INTERVIEW MODE
    # -----------------------------------------------------

    st.subheader("🎤 Interview Mode")

    mode = st.radio(
        "Choose mode:",
        [
            "Ask Questions",
            "Practice Interview",
            "Practice Test"
        ]
    )

    # -----------------------------------------------------
    # INTERVIEW CATEGORY
    # -----------------------------------------------------

    st.subheader("📂 Interview Category")

    category = st.selectbox(
        "Choose a category:",
        [
            "Python",
            "AI / Machine Learning",
            "HR Interview",
            "Data Science",
            "SQL"
        ]
    )

    st.caption(f"📌 Category: {category}")


    # -----------------------------------------------------
    # DIFFICULTY
    # -----------------------------------------------------

    st.subheader("🎯 Difficulty")

    difficulty = st.selectbox(
        "Choose difficulty:",
        [
            "All",
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    st.caption(f"🎯 Difficulty: {difficulty}")

    # -----------------------------------------------------
    # PROGRESS DASHBOARD
    # -----------------------------------------------------

    if st.button("📊 Progress Dashboard"):

        st.session_state.show_dashboard = True

    st.divider()

    # -----------------------------------------------------
    # RAG PIPELINE
    # -----------------------------------------------------

    st.subheader("🧠 RAG Pipeline")

    st.caption(
        "Embeddings: HuggingFace"
    )

    st.caption(
        "Vector Store: FAISS"
    )

    st.caption(
        "Retrieval: Multi-Query + Metadata Filtering"
    )

    st.caption(
        "Reranker: FlashRank"
    )

    st.caption(
        "LLM: TinyLlama + Ollama"
    )

    # -----------------------------------------------------
    # CLEAR CHAT
    # -----------------------------------------------------

    st.divider()

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.rerun()

    st.divider()

    # -----------------------------------------------------
    # FOOTER
    # -----------------------------------------------------

    st.caption(
        "Built with Python, LangChain, FAISS & Ollama"
    )

# ---------------------------------------------------------
# WELCOME SECTION
# ---------------------------------------------------------

st.markdown("### 👋 Welcome to your AI Career & Interview Assistant")

st.write(
    "Prepare for technical and HR interviews with "
    "AI-powered practice and resume analysis."
)

st.markdown("### 🚀 Available Features")

st.write("💬 Ask Interview Questions")
st.write("🎤 Practice Interview")
st.write("📝 Practice Test")
st.write("📊 Progress Dashboard")
st.write("📄 Resume Analysis")
st.write("🤖 AI-powered assistance")

# LOAD THE DOCUMENT
# CREATE METADATA AWARE DOCUMENTS
# INTERVIEW QUESTION DATA

documents = [

    # =========================
    # PYTHON - BEGINNER
    # =========================

    Document(
        page_content="What is a list in Python?\nA list is an ordered and changeable collection of items in Python.",
        metadata={"category": "Python", "topic": "Lists", "difficulty": "Beginner"}
    ),

    Document(
        page_content="What is a tuple in Python?\nA tuple is an ordered and immutable collection of items in Python.",
        metadata={"category": "Python", "topic": "Tuples", "difficulty": "Beginner"}
    ),

    Document(
        page_content="What is a dictionary in Python?\nA dictionary stores data in key-value pairs.",
        metadata={"category": "Python", "topic": "Dictionary", "difficulty": "Beginner"}
    ),

    Document(
        page_content="What is a function in Python?\nA function is a reusable block of code that performs a specific task.",
        metadata={"category": "Python", "topic": "Functions", "difficulty": "Beginner"}
    ),

    Document(
        page_content="What is a variable in Python?\nA variable is a name used to store a value in Python.",
        metadata={"category": "Python", "topic": "Variables", "difficulty": "Beginner"}
    ),

    # =========================
    # PYTHON - INTERMEDIATE
    # =========================

    Document(
        page_content="What is a lambda function in Python?\nA lambda function is a small anonymous function defined using the lambda keyword.",
        metadata={"category": "Python", "topic": "Lambda Functions", "difficulty": "Intermediate"}
    ),

    Document(
        page_content="What is exception handling in Python?\nException handling manages runtime errors using keywords such as try, except, else, and finally.",
        metadata={"category": "Python", "topic": "Exception Handling", "difficulty": "Intermediate"}
    ),

    Document(
        page_content="What is a list comprehension in Python?\nA list comprehension is a concise way to create a list using an expression and a loop.",
        metadata={"category": "Python", "topic": "List Comprehension", "difficulty": "Intermediate"}
    ),

    Document(
        page_content="What is the difference between == and is in Python?\nThe == operator compares values, while the is operator checks whether two references point to the same object.",
        metadata={"category": "Python", "topic": "Operators", "difficulty": "Intermediate"}
    ),

    Document(
        page_content="What is a Python module?\nA module is a Python file containing reusable code such as functions, classes, and variables.",
        metadata={"category": "Python", "topic": "Modules", "difficulty": "Intermediate"}
    ),

    # =========================
    # PYTHON - ADVANCED
    # =========================

    Document(
        page_content="What is a decorator in Python?\nA decorator is a function that modifies or extends the behavior of another function without changing its source code.",
        metadata={"category": "Python", "topic": "Decorators", "difficulty": "Advanced"}
    ),

    Document(
        page_content="What is a generator in Python?\nA generator is a special type of iterator that produces values one at a time using the yield keyword.",
        metadata={"category": "Python", "topic": "Generators", "difficulty": "Advanced"}
    ),

    Document(
        page_content="What is the Global Interpreter Lock in Python?\nThe Global Interpreter Lock, or GIL, allows only one thread to execute Python bytecode at a time in a standard CPython implementation.",
        metadata={"category": "Python", "topic": "GIL", "difficulty": "Advanced"}
    ),

    Document(
        page_content="What is a context manager in Python?\nA context manager manages resources using the with statement and commonly defines __enter__ and __exit__ methods.",
        metadata={"category": "Python", "topic": "Context Managers", "difficulty": "Advanced"}
    ),

    Document(
        page_content="What is method resolution order in Python?\nMethod Resolution Order, or MRO, determines the order in which Python searches classes when resolving methods, especially with inheritance.",
        metadata={"category": "Python", "topic": "MRO", "difficulty": "Advanced"}
    ),


    # =========================
    # AI / MACHINE LEARNING - BEGINNER
    # =========================

    Document(
        page_content="What is Artificial Intelligence?\nArtificial Intelligence is the field of creating systems that can perform tasks that normally require human intelligence.",
        metadata={"category": "AI / Machine Learning", "topic": "Artificial Intelligence", "difficulty": "Beginner"}
    ),

    Document(
        page_content="What is Machine Learning?\nMachine Learning is a branch of AI that enables computers to learn patterns from data and make predictions or decisions.",
        metadata={"category": "AI / Machine Learning", "topic": "Machine Learning", "difficulty": "Beginner"}
    ),

    Document(
        page_content="What is supervised learning?\nSupervised learning is a machine learning approach where a model learns from labeled training data.",
        metadata={"category": "AI / Machine Learning", "topic": "Supervised Learning", "difficulty": "Beginner"}
    ),

    Document(
        page_content="What is unsupervised learning?\nUnsupervised learning finds patterns or structures in data without labeled output values.",
        metadata={"category": "AI / Machine Learning", "topic": "Unsupervised Learning", "difficulty": "Beginner"}
    ),

    Document(
        page_content="What is a training dataset?\nA training dataset is the data used to teach a machine learning model to recognize patterns.",
        metadata={"category": "AI / Machine Learning", "topic": "Training Dataset", "difficulty": "Beginner"}
    ),

    # =========================
    # AI / MACHINE LEARNING - INTERMEDIATE
    # =========================

    Document(
        page_content="What is classification in machine learning?\nClassification is a supervised learning task that predicts a category or class for an input.",
        metadata={"category": "AI / Machine Learning", "topic": "Classification", "difficulty": "Intermediate"}
    ),

    Document(
        page_content="What is regression in machine learning?\nRegression is a supervised learning task used to predict continuous numerical values.",
        metadata={"category": "AI / Machine Learning", "topic": "Regression", "difficulty": "Intermediate"}
    ),

    Document(
        page_content="What is overfitting?\nOverfitting occurs when a machine learning model learns the training data too closely and performs poorly on unseen data.",
        metadata={"category": "AI / Machine Learning", "topic": "Overfitting", "difficulty": "Intermediate"}
    ),

    Document(
        page_content="What is cross-validation?\nCross-validation is a technique for evaluating a machine learning model by splitting data into multiple training and validation sets.",
        metadata={"category": "AI / Machine Learning", "topic": "Cross Validation", "difficulty": "Intermediate"}
    ),

    Document(
        page_content="What is feature engineering?\nFeature engineering is the process of creating, transforming, or selecting useful features from raw data for a machine learning model.",
        metadata={"category": "AI / Machine Learning", "topic": "Feature Engineering", "difficulty": "Intermediate"}
    ),

    # =========================
    # AI / MACHINE LEARNING - ADVANCED
    # =========================

    Document(
        page_content="What is a neural network?\nA neural network is a machine learning model made of interconnected layers of nodes that can learn complex patterns from data.",
        metadata={"category": "AI / Machine Learning", "topic": "Neural Networks", "difficulty": "Advanced"}
    ),

    Document(
        page_content="What is gradient descent?\nGradient descent is an optimization algorithm that updates model parameters to minimize a loss function.",
        metadata={"category": "AI / Machine Learning", "topic": "Gradient Descent", "difficulty": "Advanced"}
    ),

    Document(
        page_content="What is backpropagation?\nBackpropagation is an algorithm used to calculate gradients of a neural network's loss with respect to its parameters.",
        metadata={"category": "AI / Machine Learning", "topic": "Backpropagation", "difficulty": "Advanced"}
    ),

    Document(
        page_content="What is regularization in machine learning?\nRegularization adds a penalty to a model's objective function to reduce overfitting and encourage simpler models.",
        metadata={"category": "AI / Machine Learning", "topic": "Regularization", "difficulty": "Advanced"}
    ),

    Document(
        page_content="What is transfer learning?\nTransfer learning uses knowledge learned by a model on one task or dataset to help solve another related task.",
        metadata={"category": "AI / Machine Learning", "topic": "Transfer Learning", "difficulty": "Advanced"}
    ),


    # =========================
    # HR INTERVIEW - BEGINNER
    # =========================

    Document(
        page_content="Tell me about yourself.\nI am a motivated fresher with an interest in technology and programming. I am eager to learn new skills and contribute to the organization.",
        metadata={"category": "HR Interview", "topic": "Tell Me About Yourself", "difficulty": "Beginner"}
    ),

    Document(
        page_content="What are your strengths?\nMy strengths are willingness to learn, problem-solving, communication, and the ability to adapt to new situations.",
        metadata={"category": "HR Interview", "topic": "Strengths", "difficulty": "Beginner"}
    ),

    Document(
        page_content="What is your weakness?\nAs a fresher, I am still improving my practical experience, so I actively work on projects and practice my technical skills.",
        metadata={"category": "HR Interview", "topic": "Weakness", "difficulty": "Beginner"}
    ),

    Document(
        page_content="Why should we hire you?\nAs a fresher, I bring enthusiasm, willingness to learn, technical knowledge, and a strong interest in contributing to the team.",
        metadata={"category": "HR Interview", "topic": "Why Should We Hire You", "difficulty": "Beginner"}
    ),

    Document(
        page_content="Why do you want to join our company?\nI want to join a company where I can apply my skills, learn from experienced professionals, and grow professionally.",
        metadata={"category": "HR Interview", "topic": "Company Motivation", "difficulty": "Beginner"}
    ),

    # =========================
    # HR INTERVIEW - INTERMEDIATE
    # =========================

    Document(
        page_content="How do you handle criticism?\nI listen carefully to constructive criticism, understand what I can improve, and use the feedback to perform better.",
        metadata={"category": "HR Interview", "topic": "Criticism", "difficulty": "Intermediate"}
    ),

    Document(
        page_content="Describe a challenge you faced.\nDuring a project, I faced technical problems, researched possible solutions, tested different approaches, and completed the task successfully.",
        metadata={"category": "HR Interview", "topic": "Challenges", "difficulty": "Intermediate"}
    ),

    Document(
        page_content="Where do you see yourself in five years?\nI see myself as a skilled professional with stronger technical knowledge, practical experience, and greater responsibilities.",
        metadata={"category": "HR Interview", "topic": "Career Goals", "difficulty": "Intermediate"}
    ),

    Document(
        page_content="How do you handle pressure?\nI stay organized, prioritize important tasks, remain calm, and complete work step by step.",
        metadata={"category": "HR Interview", "topic": "Pressure Handling", "difficulty": "Intermediate"}
    ),

    Document(
        page_content="Why did you choose your career field?\nI chose this field because I enjoy programming, technology, and solving problems using software.",
        metadata={"category": "HR Interview", "topic": "Career Choice", "difficulty": "Intermediate"}
    ),

    # =========================
    # HR INTERVIEW - ADVANCED
    # =========================

    Document(
        page_content="How would you handle a disagreement with a teammate?\nI would listen to the teammate's viewpoint, discuss the issue calmly, focus on the project goal, and work toward a practical solution.",
        metadata={"category": "HR Interview", "topic": "Team Conflict", "difficulty": "Advanced"}
    ),

    Document(
        page_content="How would you prioritize multiple urgent tasks?\nI would evaluate deadlines, importance, dependencies, and impact, then organize the tasks and communicate if priorities conflict.",
        metadata={"category": "HR Interview", "topic": "Task Prioritization", "difficulty": "Advanced"}
    ),

    Document(
        page_content="How would you respond if you made a serious mistake at work?\nI would acknowledge the mistake, understand its impact, inform the appropriate person, correct it, and take steps to prevent it from happening again.",
        metadata={"category": "HR Interview", "topic": "Handling Mistakes", "difficulty": "Advanced"}
    ),

    Document(
        page_content="How would you adapt to a completely new technology at work?\nI would learn the fundamentals, use reliable documentation, practice with small tasks, and gradually apply the technology to the project.",
        metadata={"category": "HR Interview", "topic": "Learning New Technology", "difficulty": "Advanced"}
    ),

    Document(
        page_content="How would you handle a situation where you disagree with your manager?\nI would respectfully explain my reasoning, listen to the manager's perspective, consider the project requirements, and support the final decision professionally.",
        metadata={"category": "HR Interview", "topic": "Disagreement With Manager", "difficulty": "Advanced"}
    ),


    # =========================
    # DATA SCIENCE - BEGINNER
    # =========================

    Document(
        page_content="What is Data Science?\nData Science is the field of using data, statistics, programming, and machine learning to extract useful insights and support decisions.",
        metadata={"category": "Data Science", "topic": "Data Science", "difficulty": "Beginner"}
    ),

    Document(
        page_content="What is Pandas?\nPandas is a Python library used for data manipulation and analysis.",
        metadata={"category": "Data Science", "topic": "Pandas", "difficulty": "Beginner"}
    ),

    Document(
        page_content="What is a DataFrame?\nA DataFrame is a two-dimensional labeled data structure provided by Pandas.",
        metadata={"category": "Data Science", "topic": "DataFrame", "difficulty": "Beginner"}
    ),

    Document(
        page_content="What is data cleaning?\nData cleaning is the process of identifying and correcting missing, incorrect, duplicate, or inconsistent data.",
        metadata={"category": "Data Science", "topic": "Data Cleaning", "difficulty": "Beginner"}
    ),

    Document(
        page_content="What is data visualization?\nData visualization is the process of representing data using charts, graphs, and other visual formats.",
        metadata={"category": "Data Science", "topic": "Data Visualization", "difficulty": "Beginner"}
    ),

    # =========================
    # DATA SCIENCE - INTERMEDIATE
    # =========================

    Document(
        page_content="What is Exploratory Data Analysis?\nExploratory Data Analysis, or EDA, is the process of examining and summarizing data to discover patterns, relationships, and unusual values.",
        metadata={"category": "Data Science", "topic": "EDA", "difficulty": "Intermediate"}
    ),

    Document(
        page_content="How can missing data be handled?\nMissing data can be handled by removing affected records, filling values using suitable methods, or using algorithms that support missing values.",
        metadata={"category": "Data Science", "topic": "Missing Data", "difficulty": "Intermediate"}
    ),

    Document(
        page_content="What is correlation?\nCorrelation measures the strength and direction of the relationship between two variables.",
        metadata={"category": "Data Science", "topic": "Correlation", "difficulty": "Intermediate"}
    ),

    Document(
        page_content="What is an outlier?\nAn outlier is a data point that is unusually different from other observations in a dataset.",
        metadata={"category": "Data Science", "topic": "Outliers", "difficulty": "Intermediate"}
    ),

    Document(
        page_content="What is NumPy used for in data science?\nNumPy is a Python library that provides efficient numerical arrays and mathematical operations.",
        metadata={"category": "Data Science", "topic": "NumPy", "difficulty": "Intermediate"}
    ),

    # =========================
    # DATA SCIENCE - ADVANCED
    # =========================

    Document(
        page_content="What is normalization in data preprocessing?\nNormalization transforms numerical features to a common scale so that differences in feature ranges do not disproportionately affect a model.",
        metadata={"category": "Data Science", "topic": "Normalization", "difficulty": "Advanced"}
    ),

    Document(
        page_content="What is feature selection?\nFeature selection is the process of choosing the most relevant input variables for a model while removing unnecessary or redundant features.",
        metadata={"category": "Data Science", "topic": "Feature Selection", "difficulty": "Advanced"}
    ),

    Document(
        page_content="What is dimensionality reduction?\nDimensionality reduction reduces the number of features in a dataset while attempting to preserve important information.",
        metadata={"category": "Data Science", "topic": "Dimensionality Reduction", "difficulty": "Advanced"}
    ),

    Document(
        page_content="What is principal component analysis?\nPrincipal Component Analysis, or PCA, is a dimensionality reduction technique that transforms correlated features into a smaller set of principal components.",
        metadata={"category": "Data Science", "topic": "PCA", "difficulty": "Advanced"}
    ),

    Document(
        page_content="What is data leakage?\nData leakage occurs when information that should not be available during model training is unintentionally used, causing overly optimistic evaluation results.",
        metadata={"category": "Data Science", "topic": "Data Leakage", "difficulty": "Advanced"}
    ),


    # =========================
    # SQL - BEGINNER
    # =========================

    Document(
        page_content="What is SQL?\nSQL stands for Structured Query Language and is used to manage and query relational databases.",
        metadata={"category": "SQL", "topic": "SQL", "difficulty": "Beginner"}
    ),

    Document(
        page_content="What is a primary key?\nA primary key is a column or combination of columns that uniquely identifies each row in a table.",
        metadata={"category": "SQL", "topic": "Primary Key", "difficulty": "Beginner"}
    ),

    Document(
        page_content="What is a foreign key?\nA foreign key is a column that references a key in another table to establish a relationship between tables.",
        metadata={"category": "SQL", "topic": "Foreign Key", "difficulty": "Beginner"}
    ),

    Document(
        page_content="What is the SELECT statement in SQL?\nThe SELECT statement is used to retrieve data from one or more database tables.",
        metadata={"category": "SQL", "topic": "SELECT", "difficulty": "Beginner"}
    ),

    Document(
        page_content="What is a JOIN in SQL?\nA JOIN combines rows from two or more tables based on a related column.",
        metadata={"category": "SQL", "topic": "JOIN", "difficulty": "Beginner"}
    ),

    # =========================
    # SQL - INTERMEDIATE
    # =========================

    Document(
        page_content="What is the difference between WHERE and HAVING in SQL?\nWHERE filters rows before grouping, while HAVING filters groups after GROUP BY is applied.",
        metadata={"category": "SQL", "topic": "WHERE vs HAVING", "difficulty": "Intermediate"}
    ),

    Document(
        page_content="What is an INNER JOIN?\nAn INNER JOIN returns only the rows that have matching values in both joined tables.",
        metadata={"category": "SQL", "topic": "INNER JOIN", "difficulty": "Intermediate"}
    ),

    Document(
        page_content="What is GROUP BY in SQL?\nGROUP BY groups rows with the same values so aggregate functions can be applied to each group.",
        metadata={"category": "SQL", "topic": "GROUP BY", "difficulty": "Intermediate"}
    ),

    Document(
        page_content="What are aggregate functions in SQL?\nAggregate functions perform calculations on multiple rows and return a single result, such as COUNT, SUM, AVG, MIN, and MAX.",
        metadata={"category": "SQL", "topic": "Aggregate Functions", "difficulty": "Intermediate"}
    ),

    Document(
        page_content="What is a subquery in SQL?\nA subquery is a query nested inside another SQL query.",
        metadata={"category": "SQL", "topic": "Subquery", "difficulty": "Intermediate"}
    ),

    # =========================
    # SQL - ADVANCED
    # =========================

    Document(
        page_content="What is database normalization?\nDatabase normalization organizes data into related tables to reduce redundancy and improve data consistency.",
        metadata={"category": "SQL", "topic": "Database Normalization", "difficulty": "Advanced"}
    ),

    Document(
        page_content="What is a window function in SQL?\nA window function performs a calculation across related rows without grouping those rows into a single output row.",
        metadata={"category": "SQL", "topic": "Window Functions", "difficulty": "Advanced"}
    ),

    Document(
        page_content="What is a Common Table Expression in SQL?\nA Common Table Expression, or CTE, is a temporary named result set defined using the WITH clause that can be referenced by a SQL query.",
        metadata={"category": "SQL", "topic": "CTE", "difficulty": "Advanced"}
    ),

    Document(
        page_content="What is an index in a database?\nAn index is a database structure that can improve the speed of data retrieval operations, although it can add storage and maintenance overhead.",
        metadata={"category": "SQL", "topic": "Indexes", "difficulty": "Advanced"}
    ),

    Document(
        page_content="What is a database transaction?\nA transaction is a sequence of database operations treated as a single logical unit that can be committed or rolled back.",
        metadata={"category": "SQL", "topic": "Transactions", "difficulty": "Advanced"}
    )
]

# ADVANCED RAG SETUP
# Keep DOcuments Available For Practice Interview
chunks = documents

# Embedding Model

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Child Splitter
child_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=20
)

# Split Documents Into Smaller Chunks
child_documents = child_splitter.split_documents(
    documents
)

# FAISS Vector Store
vectorstore = FAISS.from_documents(
    child_documents,
    embeddings
)

# FlashRank reranker
reranker = FlashrankRerank()

#DISPLAY CHAT HISTORY

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# PROGRESS DASHBOARD
if st.session_state.show_dashboard:
    st.subheader("📊 Progress Dashboard")

    st.write("### 📝 Practice Test")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Tests Completed",
            st.session_state.tests_completed
        )

    with col2:
        st.metric(
            "Questions Attempted",
            st.session_state.total_test_questions
        )

    with col3:
        st.metric(
            "Total Score",
            st.session_state.total_test_score
        )

    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric(
            "Correct",
            st.session_state.total_correct_answers
        )

    with col5:
        st.metric(
            "Partially Correct",
            st.session_state.total_partial_answers
        )

    with col6:
        st.metric(
            "Incorrect",
            st.session_state.total_incorrect_answers
        )

    st.divider()

    st.write("### 🎤 Practice Interview")

    col7, col8, col9 = st.columns(3)

    with col7:
        st.metric(
            "Questions Attempted",
            st.session_state.interview_questions_attempted
        )

    with col8:
        st.metric(
            "Correct Answers",
            st.session_state.interview_correct_answers
        )

    with col9:
        st.metric(
            "Score",
            st.session_state.interview_score
        )

    st.divider()

    if st.button("⬅️ Back to Interview"):
        st.session_state.show_dashboard = False
        st.rerun()

# PRACTICE INTERVIEW MODE

if mode == "Practice Interview":

    st.subheader("🎤 Practice Interview")

    st.write(
        f"Practice your {category} interview with the AI interviewer."
    )

    # ---------------------------------------------------------
    # START INTERVIEW
    # ---------------------------------------------------------

    if st.button("▶️ Start Interview"):

        category_questions = [
            chunk
            for chunk in chunks
            if (
                chunk.metadata.get("category") == category
                and (
                    difficulty == "All"
                    or chunk.metadata.get("difficulty") == difficulty
                )
            )
        ]

        if category_questions:

            selected_question = random.choice(
                category_questions
            )

            question_answer = selected_question.page_content.split(
                "\n",
                1
            )

            if len(question_answer) >= 2:

                st.session_state.practice_question = (
                    question_answer[0].strip()
                )

                st.session_state.practice_answer_key = (
                    question_answer[1].strip()
                )

                st.session_state.practice_started = True

                st.session_state.practice_feedback = None

                st.session_state.practice_attempted = 0

                st.session_state.practice_score = 0

                st.session_state.last_submitted_question = None

                st.rerun()

            else:

                st.error(
                    "The selected interview question has an invalid format."
                )

        else:

            st.warning(
                "No interview questions found for this category."
            )

    # ---------------------------------------------------------
    # INTERVIEW STARTED
    # ---------------------------------------------------------

    if st.session_state.practice_started:

        st.info(
            "🤖 Interviewer: "
            + st.session_state.practice_question
        )

        practice_answer = st.text_area(
            "✍️ Your Answer",
            placeholder="Type your answer here...",
            key=f"practice_answer_{st.session_state.practice_question}"
        )

        col1, col2 = st.columns(2)

        # =====================================================
        # SUBMIT ANSWER
        # =====================================================

        with col1:

            if st.button("📤 Submit Answer"):

                # -------------------------------------------------
                # EMPTY ANSWER CHECK
                # -------------------------------------------------

                if not practice_answer.strip():

                    st.warning(
                        "Please enter your answer first."
                    )

                # -------------------------------------------------
                # DUPLICATE SUBMISSION CHECK
                # -------------------------------------------------

                elif (
                    st.session_state.last_submitted_question
                    == st.session_state.practice_question
                ):

                    st.warning(
                        "You have already submitted an answer "
                        "for this question. Click Next Question."
                    )

                else:

                    # -------------------------------------------------
                    # GET EXPECTED AND CANDIDATE ANSWERS
                    # -------------------------------------------------

                    expected_answer = (
                        st.session_state.practice_answer_key.strip()
                    )

                    candidate_answer = (
                        practice_answer.strip()
                    )

                    # -------------------------------------------------
                    # NORMALIZE ANSWERS
                    # -------------------------------------------------

                    expected_words = set(
                        expected_answer.lower()
                        .replace(".", "")
                        .replace(",", "")
                        .replace("?", "")
                        .replace("!", "")
                        .replace(":", "")
                        .replace(";", "")
                        .replace("(", "")
                        .replace(")", "")
                        .split()
                    )

                    candidate_words = set(
                        candidate_answer.lower()
                        .replace(".", "")
                        .replace(",", "")
                        .replace("?", "")
                        .replace("!", "")
                        .replace(":", "")
                        .replace(";", "")
                        .replace("(", "")
                        .replace(")", "")
                        .split()
                    )

                    # -------------------------------------------------
                    # COMMON WORDS
                    # -------------------------------------------------

                    common_words = {
                        "a",
                        "an",
                        "the",
                        "is",
                        "are",
                        "was",
                        "were",
                        "in",
                        "of",
                        "and",
                        "to",
                        "for",
                        "that",
                        "with",
                        "this",
                        "it",
                        "as",
                        "on",
                        "by",
                        "from",
                        "be",
                        "used",
                        "use",
                        "python"
                    }

                    expected_words = (
                        expected_words - common_words
                    )

                    candidate_words = (
                        candidate_words - common_words
                    )

                    # -------------------------------------------------
                    # CALCULATE ANSWER SIMILARITY
                    # -------------------------------------------------

                    if expected_words:

                        matching_words = (
                            expected_words.intersection(
                                candidate_words
                            )
                        )

                        similarity = (
                            len(matching_words)
                            / len(expected_words)
                        )

                    else:

                        similarity = 0

                    # -------------------------------------------------
                    # DETERMINE RESULT
                    # -------------------------------------------------

                    if similarity >= 0.70:

                        result_text = "Correct"
                        result_icon = "✅"

                        st.session_state.practice_score += 1

                        # UPDATE DASHBOARD
                        st.session_state.interview_correct_answers += 1
                        st.session_state.interview_score += 1

                    elif similarity >= 0.35:

                        result_text = "Partially Correct"
                        result_icon = "🟡"

                        st.session_state.practice_score += 0.5

                        # UPDATE DASHBOARD
                        st.session_state.interview_score += 0.5

                    else:

                        result_text = "Incorrect"
                        result_icon = "❌"

                    # -------------------------------------------------
                    # UPDATE PRACTICE INTERVIEW ATTEMPT COUNT
                    # -------------------------------------------------

                    st.session_state.practice_attempted += 1

                    # -------------------------------------------------
                    # UPDATE DASHBOARD ATTEMPT COUNT
                    # -------------------------------------------------

                    st.session_state.interview_questions_attempted += 1

                    # =================================================
                    # GENERATE CLEAN FEEDBACK
                    # =================================================

                    if result_text == "Correct":

                        feedback_text = (
                            "**What was correct:**\n"
                            "Your answer correctly explains the main "
                            "concept and includes the key point expected "
                            "for this question.\n\n"
                            "**What could be improved:**\n"
                            "Your answer is correct. In an actual interview, "
                            "you can make it stronger by adding a small "
                            "example if needed.\n\n"
                            "**Better sample answer:**\n"
                            f"{expected_answer}"
                        )

                    elif result_text == "Partially Correct":

                        feedback_text = (
                            "**What was correct:**\n"
                            "Your answer includes some of the important "
                            "concepts from the expected answer.\n\n"
                            "**What could be improved:**\n"
                            "Add the missing key points and explain the "
                            "concept a little more clearly.\n\n"
                            "**Better sample answer:**\n"
                            f"{expected_answer}"
                        )

                    else:

                        feedback_text = (
                            "**What was correct:**\n"
                            "Your answer shows an attempt to answer the "
                            "question.\n\n"
                            "**What could be improved:**\n"
                            "Review the main concept and include the key "
                            "points required to explain it correctly.\n\n"
                            "**Better sample answer:**\n"
                            f"{expected_answer}"
                        )

                    # -------------------------------------------------
                    # SAVE FEEDBACK
                    # -------------------------------------------------

                    st.session_state.practice_feedback = (
                        f"**Result:** {result_icon} {result_text}\n\n"
                        f"{feedback_text}"
                    )

                    # -------------------------------------------------
                    # REMEMBER SUBMITTED QUESTION
                    # -------------------------------------------------

                    st.session_state.last_submitted_question = (
                        st.session_state.practice_question
                    )

                    st.rerun()

        # =====================================================
        # NEXT QUESTION
        # =====================================================

        with col2:

            if st.button("➡️ Next Question"):

                category_questions = [
                    chunk
                    for chunk in chunks
                    if (
                        chunk.metadata.get("category") == category
                        and (
                            difficulty == "All"
                            or chunk.metadata.get("difficulty") == difficulty
                        )
                    )
                ]

                if category_questions:

                    current_question = (
                        st.session_state.practice_question
                    )

                    other_questions = []

                    for chunk in category_questions:

                        question_parts = (
                            chunk.page_content.split(
                                "\n",
                                1
                            )
                        )

                        if len(question_parts) >= 2:

                            question_text = (
                                question_parts[0].strip()
                            )

                            if question_text != current_question:

                                other_questions.append(
                                    chunk
                                )

                    # -------------------------------------------------
                    # SELECT DIFFERENT QUESTION
                    # -------------------------------------------------

                    if other_questions:

                        selected_question = random.choice(
                            other_questions
                        )

                    else:

                        selected_question = random.choice(
                            category_questions
                        )

                    question_answer = (
                        selected_question.page_content.split(
                            "\n",
                            1
                        )
                    )

                    if len(question_answer) >= 2:

                        st.session_state.practice_question = (
                            question_answer[0].strip()
                        )

                        st.session_state.practice_answer_key = (
                            question_answer[1].strip()
                        )

                        st.session_state.practice_feedback = None

                        st.session_state.last_submitted_question = None

                        st.rerun()

                    else:

                        st.error(
                            "The selected interview question has "
                            "an invalid format."
                        )

        # =====================================================
        # INTERVIEW FEEDBACK
        # =====================================================

        if st.session_state.practice_feedback:

            st.write("### 🤖 Interview Feedback")

            st.markdown(
                st.session_state.practice_feedback
            )

        # =====================================================
        # INTERVIEW PROGRESS
        # =====================================================

        st.write("### 📊 Interview Progress")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Questions Attempted",
                st.session_state.practice_attempted
            )

        with col2:

            st.metric(
                "🏆 Score",
                st.session_state.practice_score
            )

    st.divider()

# ---------------------------------------------------------
# PRACTICE TEST
# ---------------------------------------------------------

if mode == "Practice Test":

    st.subheader("📝 Practice Test")

    st.write(
        f"Test your {category} knowledge "
        f"with 5 interview questions."
    )

    # -----------------------------------------------------
    # START PRACTICE TEST
    # -----------------------------------------------------

    if not st.session_state.test_started:

        if st.button("▶️ Start Practice Test"):

            category_questions = [
                chunk
                for chunk in chunks
                if (
                    chunk.metadata.get("category") == category
                    and (
                        difficulty == "All"
                        or chunk.metadata.get("difficulty") == difficulty
                    )
                )
            ]

            if not category_questions:

                st.warning(
                    "⚠️ No interview questions found "
                    "for this category and difficulty."
                )

            else:

                if len(category_questions) >= 5:

                    selected_questions = random.sample(
                        category_questions,
                        5
                    )

                else:

                    selected_questions = category_questions

                    st.warning(
                        f"Only {len(category_questions)} "
                        f"questions are available for "
                        f"this category and difficulty."
                    )

                test_questions = []

                for question_data in selected_questions:

                    question_text, answer_text = (
                        question_data.page_content.split(
                            "\n",
                            1
                        )
                    )

                    test_questions.append(
                        {
                            "question": question_text,
                            "answer": answer_text
                        }
                    )

                st.session_state.test_questions = (
                    test_questions
                )

                st.session_state.test_started = True

                st.session_state.test_submitted = False

                st.session_state.test_score = 0

                st.session_state.test_results = []

                st.session_state.test_id += 1

                st.rerun()

    # -----------------------------------------------------
    # DISPLAY TEST QUESTIONS
    # -----------------------------------------------------

    if (
        st.session_state.test_started
        and not st.session_state.test_submitted
    ):

        st.write("### 📝 Answer the Questions")

        for index, question_data in enumerate(
            st.session_state.test_questions
        ):

            st.write(
                f"### Question {index + 1}"
            )

            st.write(
                question_data["question"]
            )

            answer_key = (
                f"test_answer_"
                f"{st.session_state.test_id}_"
                f"{index}"
            )

            st.text_area(
                "Your Answer:",
                key=answer_key,
                height=100
            )

            st.divider()

        # -------------------------------------------------
        # SUBMIT TEST
        # -------------------------------------------------

        if st.button("📊 Submit Test"):

            total_score = 0

            results = []

            for index, question_data in enumerate(
                st.session_state.test_questions
            ):

                answer_key = (
                    f"test_answer_"
                    f"{st.session_state.test_id}_"
                    f"{index}"
                )

                candidate_answer = st.session_state.get(
                    answer_key,
                    ""
                ).strip()

                expected_answer = (
                    question_data["answer"]
                )

                # -----------------------------------------
                # NORMALIZE WORDS
                # -----------------------------------------

                expected_words = set(
                    expected_answer.lower()
                    .replace(".", "")
                    .replace(",", "")
                    .replace("?", "")
                    .replace("!", "")
                    .replace(":", "")
                    .replace(";", "")
                    .replace("(", "")
                    .replace(")", "")
                    .split()
                )

                candidate_words = set(
                    candidate_answer.lower()
                    .replace(".", "")
                    .replace(",", "")
                    .replace("?", "")
                    .replace("!", "")
                    .replace(":", "")
                    .replace(";", "")
                    .replace("(", "")
                    .replace(")", "")
                    .split()
                )

                common_words = {
                    "a",
                    "an",
                    "the",
                    "is",
                    "are",
                    "was",
                    "were",
                    "in",
                    "of",
                    "and",
                    "to",
                    "for",
                    "that",
                    "with",
                    "this",
                    "it",
                    "as",
                    "on",
                    "by",
                    "from",
                    "be",
                    "used",
                    "use",
                    "python"
                }

                expected_words = (
                    expected_words - common_words
                )

                candidate_words = (
                    candidate_words - common_words
                )

                # -----------------------------------------
                # CALCULATE SIMILARITY
                # -----------------------------------------

                if expected_words:

                    matching_words = (
                        expected_words.intersection(
                            candidate_words
                        )
                    )

                    similarity = (
                        len(matching_words)
                        / len(expected_words)
                    )

                else:

                    similarity = 0

                # -----------------------------------------
                # RESULT
                # -----------------------------------------

                if similarity >= 0.70:

                    result = "Correct"
                    icon = "✅"
                    score = 1

                elif similarity >= 0.35:

                    result = "Partially Correct"
                    icon = "🟡"
                    score = 0.5

                else:

                    result = "Incorrect"
                    icon = "❌"
                    score = 0

                total_score += score

                results.append(
                    {
                        "question": question_data["question"],
                        "candidate_answer": candidate_answer,
                        "correct_answer": expected_answer,
                        "result": result,
                        "icon": icon,
                        "score": score
                    }
                )

            # -------------------------------------------------
            # SAVE CURRENT TEST RESULT
            # -------------------------------------------------

            st.session_state.test_score = total_score

            st.session_state.test_results = results

            st.session_state.test_submitted = True

            # -------------------------------------------------
            # UPDATE PROGRESS DASHBOARD
            # -------------------------------------------------

            st.session_state.tests_completed += 1

            st.session_state.total_test_questions += len(
                results
            )

            st.session_state.total_test_score += total_score

            st.session_state.total_correct_answers += sum(
                1
                for result in results
                if result["result"] == "Correct"
            )

            st.session_state.total_partial_answers += sum(
                1
                for result in results
                if result["result"] == "Partially Correct"
            )

            st.session_state.total_incorrect_answers += sum(
                1
                for result in results
                if result["result"] == "Incorrect"
            )

            st.rerun()

    # ---------------------------------------------------------
    # TEST RESULT
    # ---------------------------------------------------------

    if (
        st.session_state.test_started
        and st.session_state.test_submitted
    ):

        st.write("## 🎯 Test Result")

        total_questions = len(
            st.session_state.test_questions
        )

        score = st.session_state.test_score

        if total_questions > 0:

            percentage = (
                score / total_questions
            ) * 100

        else:

            percentage = 0

        correct_count = sum(
            1
            for result in st.session_state.test_results
            if result["result"] == "Correct"
        )

        partial_count = sum(
            1
            for result in st.session_state.test_results
            if result["result"] == "Partially Correct"
        )

        incorrect_count = sum(
            1
            for result in st.session_state.test_results
            if result["result"] == "Incorrect"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "🏆 Score",
                f"{score} / {total_questions}"
            )

        with col2:

            st.metric(
                "📈 Percentage",
                f"{percentage:.0f}%"
            )

        with col3:

            st.metric(
                "✅ Correct",
                correct_count
            )

        with col4:

            st.metric(
                "🟡 Partial",
                partial_count
            )

        st.write(
            f"❌ Incorrect: {incorrect_count}"
        )

        st.write("### 📋 Question Review")

        for index, result in enumerate(
            st.session_state.test_results
        ):

            st.write(
                f"### Question {index + 1}"
            )

            st.write(
                result["question"]
            )

            st.write(
                f"**Your Answer:** "
                f"{result['candidate_answer'] or 'No answer'}"
            )

            st.write(
                f"**Correct Answer:** "
                f"{result['correct_answer']}"
            )

            st.write(
                f"**Result:** "
                f"{result['icon']} "
                f"{result['result']}"
            )

            st.divider()

        # -----------------------------------------------------
        # RETAKE TEST
        # -----------------------------------------------------

        if st.button("🔄 Retake Test"):

            st.session_state.test_started = False

            st.session_state.test_questions = []

            st.session_state.test_answers = {}

            st.session_state.test_submitted = False

            st.session_state.test_score = 0

            st.session_state.test_results = []

            st.session_state.test_id += 1

            st.rerun()

    st.divider()

# NORMAL ASK QUESTION MODE

if mode == "Ask Questions":

    st.subheader("💬 Ask Interview Questions")

    query = st.chat_input(
        "Ask your interview question..."
    )

    if query is not None and query.strip():

        query = query.strip()

        # Save User Message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": query
            }
        )

        with st.chat_message("user"):
            st.write(query)

        
        # Default Values
        answer = (
            "I couldn't find this information "
            "in the selected category."
        )

        reranked_docs = []
        used_fallback = False

        # 1. Metadata Filtering
        base_retriever = vectorstore.as_retriever(
            search_kwargs={
                "k": 3,
                "filter": {
                    "category": category
                }
            }
        )

        # 2. Multi-Query Retrieval
        multi_query_retriever = MultiQueryRetriever.from_llm(
            retriever=base_retriever,
            llm=llm
        )

        retrieved_docs = multi_query_retriever.invoke(
            query
        )

        # 3. Direct Similarity Retrieval
        direct_docs = vectorstore.similarity_search(
            query,
            k=3,
            filter={
                "category": category
            }
        )


        # 4. Combine Documents
        all_docs = retrieved_docs + direct_docs

        unique_docs = []
        seen_contents = set()

        for doc in all_docs:

            content = doc.page_content.strip()

            if content not in seen_contents:

                unique_docs.append(doc)
                seen_contents.add(content)

        # 5. Topic Normalization
        def normalize_topic(text):

            text = text.lower().strip()

            for symbol in [
                "?",
                ".",
                ",",
                "!",
                ":",
                "'",
                '"'
            ]:

                text = text.replace(
                    symbol,
                    ""
                )

            # Normalize common plural forms
            if text.endswith("ies"):

                text = text[:-3] + "y"

            elif (
                text.endswith("s")
                and not text.endswith("ss")
            ):

                text = text[:-1]

            return " ".join(
                text.split()
            ).strip()

        # 6. Normalize Complete Question
        normalized_full_query = normalize_topic(
            query
        )

        # 7. Stop Words

        stop_words = {
            "what",
            "is",
            "are",
            "a",
            "an",
            "the",
            "in",
            "of",
            "to",
            "and",
            "for",
            "on",
            "with",
            "how",
            "why",
            "can",
            "does",
            "do",
            "please",
            "give",
            "difference",
            "between",
            "python",
            "sql"
        }

        # 8. Extract Important Query Words
        query_words = []

        for word in normalized_full_query.split():

            if word not in stop_words:

                query_words.append(
                    word
                )

        normalized_query = " ".join(
            query_words
        )

        # 9. Find Matching Topics
        matching_docs = []

        for doc in unique_docs:

            topic = normalize_topic(
                doc.metadata.get(
                    "topic",
                    ""
                )
            )

            if not topic:
                continue

            # ---------------------------------------------
            # FIRST: Match the complete topic against
            # the complete question.
            #
            # This is important for HR questions such as:
            #
            # "Tell me about yourself?"
            #
            # Topic:
            # "Tell me about yourself"
            # ---------------------------------------------

            if topic in normalized_full_query:

                matching_docs.append(
                    doc
                )

                continue

            # ---------------------------------------------
            # SECOND: Match against the cleaned question.
            #
            # Example:
            #
            # What is machine learning?
            # -> machine learning
            # ---------------------------------------------

            if topic == normalized_query:

                matching_docs.append(
                    doc
                )

                continue

            # ---------------------------------------------
            # THIRD: Multi-word topic matching
            # ---------------------------------------------

            if (
                len(topic.split()) > 1
                and topic in normalized_query
            ):

                matching_docs.append(
                    doc
                )

                continue

            # ---------------------------------------------
            # FOURTH: Single-word topic matching
            # ---------------------------------------------

            if (
                len(topic.split()) == 1
                and topic in query_words
            ):

                matching_docs.append(
                    doc
                )

                continue

        # 10. FlashRank Reranking
        if matching_docs:

            reranked_docs = reranker.compress_documents(
                matching_docs,
                query
            )

            if reranked_docs:

                result = reranked_docs[0]

            else:

                result = matching_docs[0]

            context = result.page_content.strip()

            # Remove the question line and show only answer
            if "\n" in context:

                answer = context.split(
                    "\n",
                    1
                )[1].strip()

            else:

                answer = context

        # 11. LLM FALLBACK
        else:

            used_fallback = True

            fallback_llm = ChatOllama(
                model="tinyllama:latest",
                temperature=0,
                num_predict=80
            )

            fallback_prompt = ChatPromptTemplate.from_template(
                """
Give a short factual answer to this question.

Question:
{question}

Answer in two simple sentences.
"""
            )

            fallback_response = fallback_llm.invoke(
                fallback_prompt.format(
                    question=query
                )
            )

            raw_answer = (
                fallback_response.content.strip()
            )

            # Remove markdown code blocks
            if "```" in raw_answer:

                raw_answer = raw_answer.split(
                    "```",
                    1
                )[0].strip()

            # Clean lines
            lines = raw_answer.splitlines()

            clean_lines = []

            for line in lines:

                line = line.strip()

                if not line:
                    continue

                # Remove numbered list items
                if line[0:2] in [
                    "1.",
                    "2.",
                    "3.",
                    "4.",
                    "5.",
                    "6.",
                    "7.",
                    "8.",
                    "9."
                ]:

                    continue

                if "do not" in line.lower():

                    continue

                clean_lines.append(
                    line
                )

            raw_answer = " ".join(
                clean_lines
            ).strip()

            # Remove unwanted labels
            if "Answer:" in raw_answer:

                raw_answer = raw_answer.split(
                    "Answer:",
                    1
                )[-1].strip()

            if "Question:" in raw_answer:

                raw_answer = raw_answer.split(
                    "Question:",
                    1
                )[-1].strip()

            # Keep maximum two useful sentences
            import re

            sentences = re.split(
                r'(?<=[.!?])\s+',
                raw_answer
            )

            useful_sentences = []

            for sentence in sentences:

                sentence = sentence.strip()

                if not sentence:
                    continue

                if "do not" in sentence.lower():
                    continue

                useful_sentences.append(
                    sentence
                )

                if len(useful_sentences) == 2:
                    break

            answer = " ".join(
                useful_sentences
            ).strip()

            if not answer:

                answer = (
                    "I couldn't generate a "
                    "reliable answer right now."
                )

        # 12. Save Assistant Answer
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        # 13. Display Assistant Answer
        with st.chat_message("assistant"):

            st.write(answer)

        
        # 14. Retrieved Context
        if (
            not used_fallback
            and reranked_docs
        ):

            with st.expander(
                "📚 Retrieved Context"
            ):

                result = reranked_docs[0]

                st.write(
                    result.page_content
                )

                st.write(
                    "**Topic:** "
                    + str(
                        result.metadata.get(
                            "topic",
                            "N/A"
                        )
                    )
                )

                st.write(
                    "**Category:** "
                    + str(
                        result.metadata.get(
                            "category",
                            "N/A"
                        )
                    )
                )

                st.write(
                    "**Difficulty:** "
                    + str(
                        result.metadata.get(
                            "difficulty",
                            "N/A"
                        )
                    )
                )

        # 15. General AI Answer
        if used_fallback:

            with st.expander(
                "🤖 General AI Answer"
            ):

                st.caption(
                    "This answer was generated "
                    "by the AI assistant."
                )

# ---------------------------------------------------------
# RESUME ANALYSIS
# ---------------------------------------------------------

st.divider()

st.subheader("📄 Resume Analysis")

st.write(
    "Upload your resume and get a clear analysis based only "
    "on the information in your resume."
)

uploaded_resume = st.file_uploader(
    "Upload your resume",
    type=["pdf", "txt"],
    key="resume_upload"
)

if uploaded_resume:

    resume_text = ""

    # -----------------------------------------------------
    # READ PDF
    # -----------------------------------------------------

    if uploaded_resume.name.lower().endswith(".pdf"):

        pdf_reader = PdfReader(uploaded_resume)

        for page in pdf_reader.pages:

            page_text = page.extract_text()

            if page_text:
                resume_text += page_text + "\n"

    # -----------------------------------------------------
    # READ TXT
    # -----------------------------------------------------

    elif uploaded_resume.name.lower().endswith(".txt"):

        resume_text = uploaded_resume.read().decode(
            "utf-8",
            errors="ignore"
        )

    resume_text = resume_text.strip()

    # -----------------------------------------------------
    # CHECK RESUME
    # -----------------------------------------------------

    if resume_text:

        st.success("✅ Resume uploaded successfully!")

        if st.button(
            "🔍 Analyze Resume",
            key="analyze_resume"
        ):

            text_lower = resume_text.lower()

            # -------------------------------------------------
            # 1. SKILLS
            # -------------------------------------------------

            skill_list = [
                "PHP",
                "HTML",
                "CSS",
                "JavaScript",
                "Bootstrap",
                "MySQL",
                "Python",
                "VS Code",
                "Microsoft Office",
                "Communication Skills"
            ]

            found_skills = []

            for skill in skill_list:

                if skill.lower() in text_lower:

                    found_skills.append(skill)

            # -------------------------------------------------
            # 2. EDUCATION
            # -------------------------------------------------

            education_lines = []

            for line in resume_text.splitlines():

                clean_line = line.strip()

                if not clean_line:
                    continue

                line_lower = clean_line.lower()

                if (
                    "matriculation" in line_lower
                    or "10th" in line_lower
                    or "p.s.e.b" in line_lower
                    or "pseb" in line_lower
                    or "diploma" in line_lower
                    or "csse" in line_lower
                    or "b.tech" in line_lower
                    or "btech" in line_lower
                ):

                    if clean_line not in education_lines:
                        education_lines.append(clean_line)

            # -------------------------------------------------
            # 3. PROJECTS
            # -------------------------------------------------

            project_lines = []

            project_names = [
                "Flat Booking",
                "Coffee Shop",
                "Traveller"
            ]

            for project in project_names:

                if project.lower() in text_lower:

                    for line in resume_text.splitlines():

                        if project.lower() in line.lower():

                            clean_line = line.strip()

                            if clean_line not in project_lines:
                                project_lines.append(clean_line)

                            break

            # -------------------------------------------------
            # 4. TRAINING
            # -------------------------------------------------

            training_lines = []

            training_keywords = [
                "industrial training",
                "future finders",
                "o7 services",
                "full stack",
                "core php",
                "mysql"
            ]

            for line in resume_text.splitlines():

                clean_line = line.strip()

                if not clean_line:
                    continue

                line_lower = clean_line.lower()

                if any(
                    keyword in line_lower
                    for keyword in training_keywords
                ):

                    if clean_line not in training_lines:
                        training_lines.append(clean_line)

            # -------------------------------------------------
            # 5. WORK EXPERIENCE
            # -------------------------------------------------

            is_fresher = "fresher" in text_lower

            # -------------------------------------------------
            # RESUME SUMMARY
            # -------------------------------------------------

            st.subheader("🤖 Resume Analysis")

            st.markdown("### 📊 Resume Summary")

            st.write(
                f"• **Skills detected:** {len(found_skills)}"
            )

            st.write(
                f"• **Education entries detected:** "
                f"{len(education_lines)}"
            )

            st.write(
                f"• **Projects detected:** "
                f"{len(project_lines)}"
            )

            st.write(
                f"• **Training entries detected:** "
                f"{len(training_lines)}"
            )

            if is_fresher:

                st.write(
                    "• **Candidate status:** Fresher"
                )

            else:

                st.write(
                    "• **Candidate status:** "
                    "Work experience information is present."
                )

            # -------------------------------------------------
            # SKILLS
            # -------------------------------------------------

            st.markdown("### 🎯 Skills Found")

            if found_skills:

                for skill in found_skills:

                    st.write(
                        f"• {skill}"
                    )

            else:

                st.write(
                    "Not mentioned in the resume."
                )

            # -------------------------------------------------
            # SKILL COVERAGE
            # -------------------------------------------------

            st.markdown("### 📈 Skill Coverage")

            total_skills = len(skill_list)
            detected_skills = len(found_skills)

            if total_skills > 0:

                skill_percentage = (
                    detected_skills / total_skills
                ) * 100

            else:

                skill_percentage = 0

            st.progress(
                skill_percentage / 100
            )

            st.write(
                f"{detected_skills} of {total_skills} "
                f"tracked skills detected "
                f"({skill_percentage:.0f}%)."
            )

            # -------------------------------------------------
            # EDUCATION
            # -------------------------------------------------

            st.markdown("### 🎓 Education")

            if education_lines:

                for education in education_lines:

                    st.write(
                        f"• {education}"
                    )

            else:

                st.write(
                    "Not mentioned in the resume."
                )

            # -------------------------------------------------
            # PROJECTS
            # -------------------------------------------------

            st.markdown("### 💻 Projects")

            if project_lines:

                for project in project_lines:

                    st.write(
                        f"• {project}"
                    )

            else:

                st.write(
                    "Not mentioned in the resume."
                )

            # -------------------------------------------------
            # TRAINING
            # -------------------------------------------------

            st.markdown("### 📚 Training")

            if training_lines:

                for training in training_lines:

                    st.write(
                        f"• {training}"
                    )

            else:

                st.write(
                    "Not mentioned in the resume."
                )

            # -------------------------------------------------
            # WORK EXPERIENCE
            # -------------------------------------------------

            st.markdown("### 💼 Work Experience")

            if is_fresher:

                st.write(
                    "• Fresher"
                )

            else:

                st.write(
                    "• Work experience information "
                    "is mentioned in the resume."
                )

            # -------------------------------------------------
            # RESUME STRENGTHS
            # -------------------------------------------------

            st.markdown("### 💪 Resume Strengths")

            strengths = []

            if found_skills:

                strengths.append(
                    "Technical skills are listed in the resume."
                )

            if project_lines:

                strengths.append(
                    "Projects are included in the resume."
                )

            if education_lines:

                strengths.append(
                    "Education information is present."
                )

            if training_lines:

                strengths.append(
                    "Training information is included."
                )

            if strengths:

                for strength in strengths:

                    st.write(
                        f"• {strength}"
                    )

            else:

                st.write(
                    "No specific resume strengths could "
                    "be detected from the available information."
                )

            # -------------------------------------------------
            # AREAS TO IMPROVE
            # -------------------------------------------------

            st.markdown("### ⚠️ Areas to Improve")

            improvement_count = 0

            if not found_skills:

                improvement_count += 1

                st.write(
                    "1. Add relevant technical skills "
                    "that are supported by your experience."
                )

            else:

                improvement_count += 1

                st.write(
                    "1. Add specific details showing how "
                    "you used your listed technical skills."
                )

            if not project_lines:

                improvement_count += 1

                st.write(
                    "2. Add relevant projects with "
                    "technologies and responsibilities."
                )

            else:

                improvement_count += 1

                st.write(
                    "2. Add your responsibilities, technologies "
                    "used, and outcomes for each project."
                )

            if not education_lines:

                improvement_count += 1

                st.write(
                    "3. Clearly mention your education details."
                )

            else:

                improvement_count += 1

                st.write(
                    "3. Keep education information clearly "
                    "organized and consistently formatted."
                )

            # -------------------------------------------------
            # RECOMMENDED INTERVIEW CATEGORIES
            # -------------------------------------------------

            st.markdown(
                "### 🧠 Recommended Interview Categories"
            )

            recommended_categories = []

            if "Python" in found_skills:

                recommended_categories.append(
                    "Python"
                )

            if (
                "PHP" in found_skills
                or "JavaScript" in found_skills
                or "HTML" in found_skills
                or "CSS" in found_skills
                or "Bootstrap" in found_skills
            ):

                recommended_categories.append(
                    "Web Development"
                )

            if "MySQL" in found_skills:

                recommended_categories.append(
                    "SQL / Database"
                )

            if project_lines:

                recommended_categories.append(
                    "Project-based questions"
                )

            if is_fresher:

                recommended_categories.append(
                    "HR Interview"
                )

            if not recommended_categories:

                recommended_categories.append(
                    "General HR Interview"
                )

            for number, topic in enumerate(
                recommended_categories,
                start=1
            ):

                st.write(
                    f"{number}. {topic}"
                )

            # -------------------------------------------------
            # INTERVIEW PREPARATION
            # -------------------------------------------------

            st.markdown(
                "### 🎤 Interview Preparation"
            )

            interview_topics = []

            if "PHP" in found_skills:

                interview_topics.append(
                    "Prepare for PHP fundamentals "
                    "and web development questions."
                )

            if (
                "HTML" in found_skills
                or "CSS" in found_skills
                or "Bootstrap" in found_skills
            ):

                interview_topics.append(
                    "Prepare for HTML, CSS and "
                    "Bootstrap questions."
                )

            if "JavaScript" in found_skills:

                interview_topics.append(
                    "Prepare for JavaScript fundamentals."
                )

            if "MySQL" in found_skills:

                interview_topics.append(
                    "Prepare for MySQL and "
                    "database fundamentals."
                )

            if "Python" in found_skills:

                interview_topics.append(
                    "Prepare for Python programming "
                    "fundamentals."
                )

            if project_lines:

                interview_topics.append(
                    "Be ready to explain your projects, "
                    "technologies used, and your contribution."
                )

            if training_lines:

                interview_topics.append(
                    "Be ready to explain what you learned "
                    "during your training."
                )

            if is_fresher:

                interview_topics.append(
                    "Prepare common HR questions for freshers."
                )

            # Add general topics until there are 5

            default_topics = [
                "Explain your technical skills "
                "with examples.",
                "Explain your education and "
                "career goals.",
                "Explain how you solve "
                "programming problems.",
                "Describe a challenging problem "
                "you solved."
            ]

            for topic in default_topics:

                if len(interview_topics) >= 5:
                    break

                if topic not in interview_topics:

                    interview_topics.append(
                        topic
                    )

            interview_topics = interview_topics[:5]

            for number, topic in enumerate(
                interview_topics,
                start=1
            ):

                st.write(
                    f"{number}. {topic}"
                )

    else:

        st.warning(
            "⚠️ Could not extract text from this resume."
        )