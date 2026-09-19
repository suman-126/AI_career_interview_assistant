#Imports
import streamlit as st
import random
from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
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
        "SQL Interview"
    ]
)

    st.write("Selected:", category)
    st.info(f"You selected: {category}")
    
    st.divider()
    
    st.caption("Built with Python, LangChain, FAISS & Ollama")

#Clear chat
    if st.button("🗑️ Clear Chat"):
       st.session_state.messages = []
       st.rerun()

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
loader = TextLoader("interview_data.txt")
documents = loader.load()

# Get the complete text
text = documents[0].page_content

# Create category sections
sections = {
    "Python": text.split("AI / MACHINE LEARNING INTERVIEW")[0],
    "AI / Machine Learning": text.split("AI / MACHINE LEARNING INTERVIEW")[1].split("HR INTERVIEW")[0],
    "HR Interview": text.split("HR INTERVIEW")[1].split("DATA SCIENCE INTERVIEW")[0],
    "Data Science": text.split("DATA SCIENCE INTERVIEW")[1].split("SQL INTERVIEW")[0],
    "SQL Interview": text.split("SQL INTERVIEW")[1]
}


# Create question-answer documents

chunks = []

for category_name, content in sections.items():

    lines = [line.strip() for line in content.strip().splitlines() if line.strip()]

    current_question = None
    current_answer = []

    for line in lines:

        is_question = (
            line.endswith("?")
            or line.startswith("Tell ")
            or line.startswith("What ")
            or line.startswith("Why ")
            or line.startswith("How ")
        )

        if is_question:

            if current_question:
                chunks.append(
                    Document(
                        page_content=f"{current_question}\n{' '.join(current_answer)}",
                        metadata={"category": category_name}
                    )
                )

            current_question = line
            current_answer = []

        else:
            if current_question:
                current_answer.append(line)

    if current_question:
        chunks.append(
            Document(
                page_content=f"{current_question}\n{' '.join(current_answer)}",
                metadata={"category": category_name}
            )
        )

#Create embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

#Faiss stores the info
vectorstore = FAISS.from_documents(
    chunks,embeddings
)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

#Practice Interview Mode
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

# Normal Ask Questions Mode
if mode == "Ask Questions":

    st.subheader("💬 Ask Your Interview Question")

    st.caption(
        "Ask a question about Python, AI, or interview preparation."
    )

    st.info(
        "💡 Type your question below and press Enter to get your answer!"
    )

    query = st.chat_input(
        "Ask your interview question..."
    )

    # Run RAG only when a question is entered
    if query is not None and query.strip():

        query = query.strip()

        # Store the chat history
        st.session_state.messages.append({
            "role": "user",
            "content": query
        })

        st.chat_message("user").write(query)

        results_with_scores = vectorstore.similarity_search_with_score(
            query,
            k=1,
            filter={"category": category}
        )

        if not results_with_scores:

            st.warning(
                "No relevant information found."
            )

            st.stop()

        result, score = results_with_scores[0]

        if score < 1.0:

            context = result.page_content

            answer = context.split(
                "\n",
                1
            )[1].strip()

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

            with st.chat_message("assistant"):
                st.write(answer)

        else:

            st.write(
                "💡 I couldn't find this question in the interview "
                "knowledge base, so I'll answer it using general AI knowledge."
            )

            response = llm.invoke(query)

            st.session_state.messages.append({
                "role": "assistant",
                "content": response.content
            })

            with st.chat_message("assistant"):
                st.write(response.content)
# Resume Analysis
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


