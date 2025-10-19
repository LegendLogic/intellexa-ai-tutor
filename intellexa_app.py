%%writefile intellexa_app.py
import streamlit as st
import os, requests, json
from datetime import datetime, timedelta

# =============================
#  Intellexa AI Tutor Settings
# =============================
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_ID = "gpt-4o-mini"   # ✅ stable free model

st.set_page_config(page_title="Intellexa AI Tutor", layout="wide")

st.title("🧠 Intellexa — Adaptive AI Learning Tutor")
st.caption("Personalized AI Learning Assistant — Powered by OpenRouter GPT")

# ========== USER INPUT ==========
with st.sidebar:
    st.header("🎯 User Settings")
    name = st.text_input("Enter your name", "")
    goal = st.selectbox(
        "Choose your Goal",
        ["Data Analytics","Web Development","Machine Learning","Data Science",
         "MERN Stack","Java Development","Android Development"]
    )
    level = st.selectbox("Skill Level", ["Beginner", "Intermediate", "Advanced"])
    hours = st.slider("Study Time (hours/day)", 1, 6, 2)
    days = st.slider("Number of Days for Completion", 5, 30, 10)

# ========== LEARNING PLAN ==========
if name:
    st.subheader(f"📅 {goal} Learning Plan for {name}")
    plan = []
    topics = {
        "Data Analytics":["Python Basics","SQL","Data Cleaning","Visualization","Project"],
        "Web Development":["HTML/CSS","JavaScript","Frontend Frameworks","Backend Basics","Mini Project"],
        "Machine Learning":["Python & Numpy","Pandas & Matplotlib","Supervised ML","Unsupervised ML","ML Project"],
        "Data Science":["Statistics","Python for DS","EDA","ML Algorithms","Capstone Project"],
        "MERN Stack":["MongoDB","Express.js","React.js","Node.js","Full-stack Project"],
        "Java Development":["Core Java","OOP Concepts","Spring Boot","Database Connectivity","Project"],
        "Android Development":["Java/Kotlin Basics","Android Studio UI","APIs & Firebase","App Deployment","Final Project"]
    }

    topic_list = topics.get(goal, [])
    for i in range(days):
        topic = topic_list[i % len(topic_list)]
        plan.append({
            "Day": f"Day {i+1}",
            "Topic": topic,
            "Activity": f"Learn and practice {topic.lower()}",
            "Goal": f"Complete exercises on {topic.lower()}"
        })

    st.table(plan)

    # ========== AI Tutor ==========
    st.subheader("🤖 AI Tutor Assistant")
    chosen_topic = st.selectbox("Select a Topic to Learn More", topic_list)
    action = st.radio(
        "Choose what you want the AI to do",
        ["Explain Topic Clearly","Generate Practice Questions",
         "Suggest Next Topic","Give Study Improvement Tips"]
    )

    if st.button("Ask AI ✨"):
        with st.spinner("Thinking..."):
            prompt = f"You are an AI tutor for {goal}. {action} about {chosen_topic} for a {level} learner."
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": MODEL_ID,
                "messages": [{"role": "user", "content": prompt}]
            }
            try:
                r = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                if r.status_code == 200:
                    result = r.json()["choices"][0]["message"]["content"]
                    st.success(result)
                else:
                    st.error(f"❌ OpenRouter API Error: {r.status_code} — {r.text}")
            except Exception as e:
                st.error(f"❌ Request failed: {e}")
