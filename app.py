import streamlit as st
import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Interview Assistant", layout="wide")
st.title("🎯 AI Interview Assistant")

# Initialize session state
if "question" not in st.session_state:
    st.session_state.question = ""
if "answer" not in st.session_state:
    st.session_state.answer = ""
if "feedback" not in st.session_state:
    st.session_state.feedback = ""

# Sidebar settings
with st.sidebar:
    st.header("⚙️ Settings")
    job_role = st.text_input("Job Role", "Software Engineer")
    experience = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Advanced"])

# Main layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Question")
    
    if st.button("🔄 Generate Question", use_container_width=True):
        with st.spinner("Generating question..."):
            prompt = f"""Generate ONE {experience.lower()} level interview question for a {job_role} position.
            Make it clear and concise. Only return the question."""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            st.session_state.question = response.choices[0].message.content
            st.session_state.feedback = ""
    
    if st.session_state.question:
        st.info(st.session_state.question)

with col2:
    st.subheader("💬 Your Answer")
    
    user_answer = st.text_area("Type your answer here:", height=200, key="user_input")
    
    if st.button("✅ Evaluate Answer", use_container_width=True):
        if not st.session_state.question:
            st.error("Please generate a question first!")
        elif not user_answer.strip():
            st.error("Please enter an answer!")
        else:
            with st.spinner("Evaluating your answer..."):
                eval_prompt = f"""
                Interview Question: {st.session_state.question}
                
                Candidate's Answer: {user_answer}
                
                Please evaluate this answer and provide:
                1. Score (out of 10)
                2. What went well (Strengths)
                3. What could be better (Areas to improve)
                4. A sample better answer
                
                Format your response clearly with these 4 sections."""
                
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": eval_prompt}],
                    temperature=0.5
                )
                st.session_state.feedback = response.choices[0].message.content

# Display feedback
if st.session_state.feedback:
    st.divider()
    st.subheader("📊 Feedback")
    st.success(st.session_state.feedback)