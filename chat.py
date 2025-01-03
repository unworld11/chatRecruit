import streamlit as st
from groq import Groq

# Initialize Groq client
client = Groq(api_key="YOUR_API_KEY")


# Session state keys for better organization
SESSION_KEYS = {
    "context": "conversation_context",
    "active": "chat_active",
    "candidate": "candidate_info",
    "questions": "technical_questions",
    "current_question_index": "current_q_index",
    "all_questions_answered": "all_q_answered",
}

# Initialize session state
if SESSION_KEYS["context"] not in st.session_state:
    st.session_state[SESSION_KEYS["context"]] = []
if SESSION_KEYS["active"] not in st.session_state:
    st.session_state[SESSION_KEYS["active"]] = False
if SESSION_KEYS["candidate"] not in st.session_state:
    st.session_state[SESSION_KEYS["candidate"]] = {}
if SESSION_KEYS["questions"] not in st.session_state:
    st.session_state[SESSION_KEYS["questions"]] = []
if SESSION_KEYS["current_question_index"] not in st.session_state:
    st.session_state[SESSION_KEYS["current_question_index"]] = 0
if SESSION_KEYS["all_questions_answered"] not in st.session_state:
    st.session_state[SESSION_KEYS["all_questions_answered"]] = False

# --- Helper Functions ---
def update_context(role, content):
    st.session_state[SESSION_KEYS["context"]].append({"role": role, "content": content})

def clear_context():
    st.session_state[SESSION_KEYS["context"]] = []

def get_candidate_info():
    return st.session_state.get(SESSION_KEYS["candidate"], {})

def set_candidate_info(info):
    st.session_state[SESSION_KEYS["candidate"]] = info
    # No automatic start, wait for explicit button click
    clear_context()

def format_candidate_info(info):
    formatted_info = "\n".join(
        f"- {key.title()}: {value}" for key, value in info.items()
    )
    return formatted_info

def end_conversation(message="Thank you for your time! We'll review your application and get back to you soon."):
    st.session_state[SESSION_KEYS["active"]] = False
    clear_context()
    return message

def generate_response(user_input, model="llama-3.3-70b-versatile"):
    messages = st.session_state[SESSION_KEYS["context"]] + [
        {"role": "user", "content": user_input}
    ]
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
            top_p=0.9,
            stream=False,
            stop=None,
        )
        response = completion.choices[0].message.content.strip()
        return response
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return "I'm sorry, I encountered an error. Please try again later."

# --- Specialized Functions ---
def generate_technical_questions(tech_stack, num_questions=3):
    if not tech_stack:
        return ["Please specify your tech stack to generate technical questions."]

    prompt = f"Generate {num_questions} technical interview questions for a candidate with expertise in the following technologies: {', '.join(tech_stack)}. Each question should be concise and focus on a specific technical concept or problem-solving scenario related to these technologies."

    messages = [
        {"role": "system", "content": "You are a technical recruiter generating interview questions"},
        {"role": "user", "content": prompt}
    ]

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=500,
            top_p=0.9,
            stream=False,
            stop=None
        )
        response = completion.choices[0].message.content.strip()
        questions = [q.strip() for q in response.split("\n") if q.strip() and q.strip()[0].isdigit()]
        return questions
    except Exception as e:
        return [f"Error generating questions: {str(e)}"]

def check_answer(question_index, answer):
    """Simple keyword-based answer checking (improve this!)."""
    question = st.session_state[SESSION_KEYS["questions"]][question_index]
    question_lower = question.lower()
    answer_lower = answer.lower()

    # Add more sophisticated checks here based on keywords or patterns
    if "what is" in question_lower and any(keyword in answer_lower for keyword in ["explain", "define", "refers to"]):
        return True
    elif "how to" in question_lower and any(keyword in answer_lower for keyword in ["method", "way", "using"]):
        return True
    elif "difference between" in question_lower and "vs" in answer_lower:
        return True
    return False

# --- Streamlit UI ---
st.title("AI-Powered Recruitment Chatbot")

# --- Candidate Information Collection ---
if not st.session_state[SESSION_KEYS["active"]]:
    with st.container():
        st.write("### Candidate Information")
        st.write("Please provide the following information to get started.")

        info = {}
        col1, col2 = st.columns(2)
        info["full_name"] = col1.text_input("Full Name")
        info["email"] = col1.text_input("Email Address")
        info["phone"] = col1.text_input("Phone Number")
        info["experience"] = col1.number_input("Years of Experience", min_value=0, step=1)
        info["desired_position"] = col2.text_input("Desired Position(s)")
        info["current_location"] = col2.text_input("Current Location")
        info["tech_stack"] = col2.multiselect(
            "Tech Stack (select all that apply)",
            options=[
                "Python", "JavaScript", "Java", "C++", "C#", "Ruby", "Go", "Rust",
                "React", "Angular", "Vue.js", "Node.js", "Express.js", "Django", "Flask", "Ruby on Rails",
                "Spring", "Spring Boot",
                "SQL", "NoSQL", "MongoDB", "PostgreSQL", "MySQL", "Cassandra",
                "AWS", "Azure", "Google Cloud Platform",
                "Docker", "Kubernetes", "Git",
                "Other"
            ],
        )
        info["other_tech"] = col2.text_input("If 'Other' is selected above, please specify:")

        if st.button("Submit Information"):
            if info["other_tech"]:
                info["tech_stack"].append(info["other_tech"])
            del info["other_tech"]

            set_candidate_info(info)
            st.session_state[SESSION_KEYS["questions"]] = generate_technical_questions(info["tech_stack"], num_questions=3)
            st.success("Thank you! Your information has been submitted.")
            st.balloons()

        if get_candidate_info() and not st.session_state[SESSION_KEYS["active"]]:
            if st.button("Start Chat & Technical Questions"):
                st.session_state[SESSION_KEYS["active"]] = True
                clear_context()
                greeting = f"Welcome, {get_candidate_info().get('full_name')}. Let's start with some technical questions."
                update_context("assistant", greeting)
                st.rerun()  # Force a rerun to display the chat interface

# --- Chat Interface ---
if st.session_state[SESSION_KEYS["active"]]:
    candidate_info = get_candidate_info()

    st.write("### Candidate Information Summary")
    st.write(format_candidate_info(candidate_info))

    st.write("### Technical Interview")

    if st.session_state[SESSION_KEYS["questions"]]:
        question_index = st.session_state[SESSION_KEYS["current_question_index"]]
        if question_index < len(st.session_state[SESSION_KEYS["questions"]]):
            current_question = st.session_state[SESSION_KEYS["questions"]][question_index]
            st.write(f"**Question {question_index + 1}/{len(st.session_state[SESSION_KEYS['questions']])}:** {current_question}")
            answer = st.text_input("Your Answer")

            col1, col2 = st.columns(2)
            if col1.button("Submit Answer"):
                if answer.strip():
                    is_correct = check_answer(question_index, answer)
                    if is_correct:
                        st.success("Correct!")
                    else:
                        st.error("That's not quite right.")

                    st.session_state[SESSION_KEYS["current_question_index"]] += 1
                    st.rerun() # Move to the next question

        else:
            st.success("Congratulations! You've answered all the technical questions.")
            st.session_state[SESSION_KEYS["all_questions_answered"]] = True

    if st.session_state[SESSION_KEYS["all_questions_answered"]]:
        st.write("### General Chat (Optional)")
        user_input = st.text_input("Your message", key="user_input")

        col1, col2 = st.columns([2, 1])
        if col1.button("Send", type="primary"):
            if user_input.strip():
                update_context("user", user_input)
                with st.chat_message("user"):
                    st.markdown(user_input)

                with st.chat_message("assistant"):
                    placeholder = st.empty()
                    placeholder.markdown("Thinking...")
                    response = generate_response(user_input)
                    placeholder.markdown(response)
                    update_context("assistant", response)

        if col2.button("End Chat"):
            end_message = end_conversation()
            update_context("assistant", end_message)
            with st.chat_message("assistant"):
                st.markdown(end_message)
            st.session_state[SESSION_KEYS["active"]] = False
            st.rerun() # End the chat session

# --- Conversation History (Move to the bottom for better flow) ---
if st.session_state[SESSION_KEYS["context"]] and st.session_state[SESSION_KEYS["all_questions_answered"]]:
    with st.expander("Conversation History", expanded=False):
        for msg in st.session_state[SESSION_KEYS["context"]]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
