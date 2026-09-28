#Imports
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

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Practice Interview state
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

#Import the model of chatollama
llm = ChatOllama(
    model="tinyllama:latest",
    temperature=0,
    num_predict=500
)
#Title
#Custom CSS
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 38px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .subtitle {
        text-align: center;
        font-size: 17px;
        margin-bottom: 25px;
    }
     .welcome-box {
        padding: 20px;
        border-radius: 12px;
        margin-top: 10px;
        margin-bottom: 25px;
        border: 1px solid rgba(128, 128, 128, 0.3);
    }

    .welcome-box h3 {
        margin-top: 0;
    }

    .welcome-box p {
        margin-bottom: 8px;
    }

    .welcome-box li {
        margin-bottom: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
#Title
st.markdown(
    '<div class="main-title">🤖 AI Career & Interview Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your AI-powered interview preparation assistant</div>',
    unsafe_allow_html=True
)

#Sidebar
with st.sidebar:
    st.header("🤖 AI Interview Assistant")
    
    st.write("Prepare for your interviews with AI-powered assistance.")
    st.divider()
    
    st.subheader("📚 Knowledge Base")
    st.write("Interview Data")
    
    st.subheader("⚡ Features")
    st.write("• Interview Questions")
    st.write("• AI-powered Answers")
    st.write("• Document-based Answers")
    st.write("• General AI Assistance")

#Interview Category
    st.subheader("🎤 Interview Mode")

    mode = st.radio(
    "Choose mode:",
    ["Ask Questions", "Practice Interview"]
)
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

    st.write("Selected:", category)
    st.info(f"You selected: {category}")
    
    st.sidebar.divider()
    
    st.sidebar.subheader("🧠 RAG Pipeline")
    
    st.sidebar.caption("Embeddings: HuggingFace")
    st.sidebar.caption("Vector Store: FAISS")
    st.sidebar.caption("Retrieval:Multi-Query + Metadata Filtering")
    st.sidebar.caption("Reranker: FlashRank")
    st.sidebar.caption("LLM: TinyLlama + Ollama")
    
    #Clear chat
    st.divider()

    if st.button("🗑️ Clear Chat"):
       st.session_state.messages = []
       st.rerun()

    st.divider()
    
    st.caption("Built with Python, LangChain, FAISS & Ollama")

#Welcome Section
st.markdown(
    """
    <div class="welcome-box">
        <h3>👋 Welcome to your AI Career & Interview Assistant</h3>
        <p>Ask me any interview question and I will help you prepare.</p>
        <p><b>You can ask about:</b></p>
        <ul>
            <li>🐍 Python</li>
            <li>💼 Interview questions</li>
            <li>🤖 AI and technology</li>
            <li>📚 General career topics</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

#Load the Document
# Create metadata-aware documents
documents = [
    Document(
        page_content="What is a list in Python?\nA list is an ordered and changeable collection of items in Python.",
        metadata={
            "category": "Python",
            "topic": "Lists",
            "difficulty": "Beginner"
        }
    ),

    Document(
        page_content="What is a tuple in Python?\nA tuple is an ordered and unchangeable collection of items in Python.",
        metadata={
            "category": "Python",
            "topic": "Tuples",
            "difficulty": "Beginner"
        }
    ),

    Document(
        page_content="What is a dictionary in Python?\nA dictionary stores data in key-value pairs.",
        metadata={
            "category": "Python",
            "topic": "Dictionary",
            "difficulty": "Beginner"
        }
    ),

    Document(
        page_content="What is a function in Python?\nA function is a reusable block of code that performs a specific task.",
        metadata={
            "category": "Python",
            "topic": "Functions",
            "difficulty": "Beginner"
        }
    ),

    Document(
        page_content="What is Artificial Intelligence?\nArtificial Intelligence is the ability of machines to perform tasks that normally require human intelligence.",
        metadata={
            "category": "AI / Machine Learning",
            "topic": "Artificial Intelligence",
            "difficulty": "Beginner"
        }
    ),

    Document(
        page_content="What is Machine Learning?\nMachine Learning is a branch of AI that allows computers to learn patterns from data and make predictions.",
        metadata={
            "category": "AI / Machine Learning",
            "topic": "Machine Learning",
            "difficulty": "Beginner"
        }
    ),

    Document(
        page_content="Tell me about yourself.\nI am a motivated fresher with an interest in technology and programming. I am eager to learn new skills and grow professionally.",
        metadata={
            "category": "HR Interview",
            "topic": "Tell me about yourself",
            "difficulty": "Beginner"
        }
    ),

    Document(
        page_content="What are your strengths?\nMy strengths are that I am a quick learner, hardworking, and willing to improve my skills.",
        metadata={
            "category": "HR Interview",
            "topic": "Strengths",
            "difficulty": "Beginner"
        }
    ),

    Document(
        page_content="What is Data Science?\nData Science is the field of extracting useful insights and knowledge from data.",
        metadata={
            "category": "Data Science",
            "topic": "Data Science",
            "difficulty": "Beginner"
        }
    ),

    Document(
        page_content="What is Pandas?\nPandas is a Python library used for data manipulation and analysis.",
        metadata={
            "category": "Data Science",
            "topic": "Pandas",
            "difficulty": "Beginner"
        }
    ),

    Document(
        page_content="What is SQL?\nSQL is a language used to manage and query data stored in databases.",
        metadata={
            "category": "SQL",
            "topic": "SQL",
            "difficulty": "Beginner"
        }
    ),

    Document(
        page_content="What is a primary key?\nA primary key uniquely identifies each record in a database table.",
        metadata={
            "category": "SQL",
            "topic": "Primary Key",
            "difficulty": "Beginner"
        }
    ),

    Document(
        page_content="What is a foreign key?\nA foreign key is a field that connects one table to another table.",
        metadata={
            "category": "SQL",
            "topic": "Foreign Key",
            "difficulty": "Beginner"
        }
    ),

    Document(
        page_content="What is the difference between WHERE and HAVING?\nWHERE filters rows before grouping, while HAVING filters groups after grouping.",
        metadata={
            "category": "SQL",
            "topic": "WHERE vs HAVING",
            "difficulty": "Beginner"
        }
    )
]

# ADVANCED RAG SETUP

# Keep documents available for Practice Interview
chunks = documents

# Embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Child splitter
child_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=20
)

# Split documents into smaller chunks
child_documents = child_splitter.split_documents(
    documents
)

# FAISS vector store
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

#PRACTICE INTERVIEW MODE
if mode == "Practice Interview":

    st.subheader("🎤 Practice Interview")

    st.write(
        f"Practice your {category} interview with the AI interviewer."
    )

    # Start Interview
    if st.button("▶️ Start Interview"):

        category_questions = [
            chunk
            for chunk in chunks
            if chunk.metadata.get("category") == category
        ]

        if category_questions:

            selected_question = random.choice(category_questions)

            question_answer = selected_question.page_content.split(
                "\n", 1
            )

            st.session_state.practice_question = question_answer[0]

            st.session_state.practice_answer_key = question_answer[1]

            st.session_state.practice_started = True

            st.session_state.practice_feedback = None

            st.session_state.practice_attempted = 0

            st.session_state.practice_score = 0

            st.rerun()

        else:

            st.warning(
                "No interview questions found for this category."
            )

    # Interview started
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

        # Submit Answer
        with col1:

            if st.button("📤 Submit Answer"):

                if practice_answer.strip():

                    st.session_state.practice_attempted += 1

                    evaluation_prompt = f"""
You are an interview coach.

Interview Question:
{st.session_state.practice_question}

Expected Answer:
{st.session_state.practice_answer_key}

Candidate Answer:
{practice_answer}

Evaluate the candidate's answer.

Give:
1. What was correct
2. What could be improved
3. A better sample answer

Keep the feedback simple and short.
"""

                    feedback = llm.invoke(
                        evaluation_prompt
                    )

                    st.session_state.practice_feedback = (
                        feedback.content
                    )

                    st.session_state.practice_score += 1

                else:

                    st.warning(
                        "Please enter your answer first."
                    )

        # Next Question
        with col2:

            if st.button("➡️ Next Question"):

                category_questions = [
                    chunk
                    for chunk in chunks
                    if chunk.metadata.get("category") == category
                ]

                if category_questions:

                    selected_question = random.choice(
                        category_questions
                    )

                    question_answer = selected_question.page_content.split(
                        "\n", 1
                    )

                    st.session_state.practice_question = (
                        question_answer[0]
                    )

                    st.session_state.practice_answer_key = (
                        question_answer[1]
                    )

                    # Remove old feedback
                    st.session_state.practice_feedback = None

                    st.rerun()

        # Feedback
        if st.session_state.practice_feedback:

            st.write("### 🤖 Interview Feedback")

            st.write(
                st.session_state.practice_feedback
            )

        # Progress
        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "📊 Questions Attempted",
                st.session_state.practice_attempted
            )

        with col2:

            st.metric(
                "🏆 Score",
                st.session_state.practice_score
            )

    st.divider()

# =========================
# Normal Ask Questions Mode
# =========================

if mode == "Ask Questions":

    st.subheader("💬 Ask Interview Questions")

    query = st.chat_input(
        "Ask your interview question..."
    )

    if query is not None and query.strip():

        query = query.strip()

        # -------------------------------------------------
        # Save user message
        # -------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": query
            }
        )

        with st.chat_message("user"):
            st.write(query)

        # -------------------------------------------------
        # Default values
        # -------------------------------------------------

        answer = (
            "I couldn't find this information "
            "in the selected category."
        )

        reranked_docs = []
        used_fallback = False

        # =================================================
        # 1. Metadata Filtering
        # =================================================

        base_retriever = vectorstore.as_retriever(
            search_kwargs={
                "k": 3,
                "filter": {
                    "category": category
                }
            }
        )

        # =================================================
        # 2. Multi-Query Retrieval
        # =================================================

        multi_query_retriever = MultiQueryRetriever.from_llm(
            retriever=base_retriever,
            llm=llm
        )

        retrieved_docs = multi_query_retriever.invoke(
            query
        )

        # =================================================
        # 3. Direct Similarity Retrieval
        # =================================================

        direct_docs = vectorstore.similarity_search(
            query,
            k=3,
            filter={
                "category": category
            }
        )

        # =================================================
        # 4. Combine Documents
        # =================================================

        all_docs = retrieved_docs + direct_docs

        unique_docs = []
        seen_contents = set()

        for doc in all_docs:

            content = doc.page_content.strip()

            if content not in seen_contents:

                unique_docs.append(doc)
                seen_contents.add(content)

        # =================================================
        # 5. Topic Normalization
        # =================================================

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

        # =================================================
        # 6. Normalize Complete Question
        # =================================================

        normalized_full_query = normalize_topic(
            query
        )

        # =================================================
        # 7. Stop Words
        # =================================================

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

        # =================================================
        # 8. Extract Important Query Words
        # =================================================

        query_words = []

        for word in normalized_full_query.split():

            if word not in stop_words:

                query_words.append(
                    word
                )

        normalized_query = " ".join(
            query_words
        )

        # =================================================
        # 9. Find Matching Topics
        # =================================================

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

        # =================================================
        # 10. FlashRank Reranking
        # =================================================

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

            # ---------------------------------------------
            # Remove the question line and show only answer
            # ---------------------------------------------

            if "\n" in context:

                answer = context.split(
                    "\n",
                    1
                )[1].strip()

            else:

                answer = context

        # =================================================
        # 11. LLM FALLBACK
        # =================================================

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

            # ---------------------------------------------
            # Remove markdown code blocks
            # ---------------------------------------------

            if "```" in raw_answer:

                raw_answer = raw_answer.split(
                    "```",
                    1
                )[0].strip()

            # ---------------------------------------------
            # Clean lines
            # ---------------------------------------------

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

            # ---------------------------------------------
            # Remove unwanted labels
            # ---------------------------------------------

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

            # ---------------------------------------------
            # Keep maximum two useful sentences
            # ---------------------------------------------

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

        # =================================================
        # 12. Save Assistant Answer
        # =================================================

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        # =================================================
        # 13. Display Assistant Answer
        # =================================================

        with st.chat_message("assistant"):

            st.write(answer)

        # =================================================
        # 14. Retrieved Context
        # =================================================

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

        # =================================================
        # 15. General AI Answer
        # =================================================

        if used_fallback:

            with st.expander(
                "🤖 General AI Answer"
            ):

                st.caption(
                    "This answer was generated "
                    "by the AI assistant."
                )

                
# =========================
# Resume Analysis
# =========================
st.divider()

st.subheader("📄 Resume Analysis")

st.write(
    "Upload your resume and get a clear analysis based only on the information in your resume."
)

uploaded_resume = st.file_uploader(
    "Upload your resume",
    type=["pdf", "txt"],
    key="resume_upload"
)

if uploaded_resume:

    resume_text = ""

    # Read PDF
    if uploaded_resume.name.lower().endswith(".pdf"):

        pdf_reader = PdfReader(uploaded_resume)

        for page in pdf_reader.pages:

            page_text = page.extract_text()

            if page_text:
                resume_text += page_text + "\n"

 
    # Read TXT

    elif uploaded_resume.name.lower().endswith(".txt"):

        resume_text = uploaded_resume.read().decode(
            "utf-8",
            errors="ignore"
        )

    resume_text = resume_text.strip()

    
    # Check resume
    
    if resume_text:

        st.success("✅ Resume uploaded successfully!")

        if st.button(
            "🔍 Analyze Resume",
            key="analyze_resume"
        ):

            text_lower = resume_text.lower()

        
            # 1. SKILLS
    
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

            
            # 2. EDUCATION
    

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

            
            # 3. PROJECTS
        

            project_lines = []

            project_names = [
                "Flat Booking",
                "Coffee Shop",
                "Traveller"
            ]

            for project in project_names:

                if project.lower() in text_lower:

                    # Find the line containing the project
                    for line in resume_text.splitlines():

                        if project.lower() in line.lower():

                            clean_line = line.strip()

                            if clean_line not in project_lines:
                                project_lines.append(clean_line)

                            break

            
            # 4. TRAINING

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

        
            # 5. WORK EXPERIENCE
        
            is_fresher ="fresher" in text_lower
        
            
            # DISPLAY ANALYSIS
            

            st.subheader("🤖 Resume Analysis")

        
            # Skills
            

            st.markdown("### 🎯 Skills Found")

            if found_skills:

                for skill in found_skills:
                    st.write(f"• {skill}")

            else:

                st.write(
                    "Not mentioned in the resume."
                )

            # Education
        
            st.markdown("### 🎓 Education")

            if education_lines:

                for education in education_lines:
                    st.write(f"• {education}")

            else:

                st.write(
                    "Not mentioned in the resume."
                )


            # Projects
            
            st.markdown("### 💻 Projects")

            if project_lines:

                for project in project_lines:
                    st.write(f"• {project}")

            else:

                st.write(
                    "Not mentioned in the resume."
                )

            
            # Training
        

            st.markdown("### 📚 Training")

            if training_lines:

                for training in training_lines:
                    st.write(f"• {training}")

            else:

                st.write(
                    "Not mentioned in the resume."
                )

            # Work Experience
        
            st.markdown("### 💼 Work Experience")

            if is_fresher:

                st.write(
                    "• Fresher"
                )

            else:

                st.write(
                    "• Work experience is mentioned in the resume."
                )

            
            # AREAS TO IMPROVE
        

            st.markdown("### ⚠️ Areas to Improve")

            st.write(
                "1. Add a clear professional summary focused on your target software-development role."
            )

            st.write(
                "2. Add more specific details about your projects, including your responsibilities and technologies used."
            )

            st.write(
                "3. Keep the education, training, participation, and experience sections clearly organized and consistently formatted."
            )

            
            # INTERVIEW PREPARATION
        
            st.markdown("### 🎤 Interview Preparation")

            interview_topics = []

            if "PHP" in found_skills:
                interview_topics.append(
                    "PHP fundamentals and web development"
                )

            if "HTML" in found_skills:
                interview_topics.append(
                    "HTML, CSS and Bootstrap"
                )

            if "JavaScript" in found_skills:
                interview_topics.append(
                    "JavaScript fundamentals"
                )

            if "MySQL" in found_skills:
                interview_topics.append(
                    "MySQL and database fundamentals"
                )

            if project_lines:
                interview_topics.append(
                    "Questions about your projects and your role in them"
                )

            # Make exactly 5 topics
            default_topics = [
                "Explain your technical skills and how you have used them.",
                "Explain your industrial training and what you learned.",
                "Explain your education and career goals.",
                "Explain how you solve programming problems."
            ]

            for topic in default_topics:

                if len(interview_topics) >= 5:
                    break

                if topic not in interview_topics:
                    interview_topics.append(topic)

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

