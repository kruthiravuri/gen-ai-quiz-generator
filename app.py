mport streamlit as st
from pydantic import BaseModel, Field
from typing import List
import os
from google import genai
from google.genai import types

# ==========================================
# 1. STRICT DATA SCHEMAS (Pydantic Layer)
# ==========================================
class QuizQuestion(BaseModel):
    question_text: str = Field(description="The multiple choice question text.")
    options: List[str] = Field(description="Exactly 4 distinct multiple choice options.")
    correct_option_index: int = Field(description="The index (0 to 3) of the correct answer in the options list.")
    explanation: str= Field(description="A short explanation explaining why the answer is correct.")

class QuizResponse(BaseModel):
    topic: str
    difficulty: str
    questions: List[QuizQuestion]

# ==========================================
# 2. GENERATION LAYER (Gemini AI Client)
# ==========================================
# Replace "YOUR_API_KEY_HERE" with your free key from Google AI Studio
# Alternatively, set it as an environment variable in your terminal
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")


def generate_quiz(topic: st, difficulty: st, count: int) -> QuizResponse:
    """Calls Gemini with a strict structural JSON schema guarantee."""
    client = genai.Client()
    prompt = f"""
    You are an expert academic evaluator. Create a high-quality multiple choice quiz 
    on the topic of '{topic}' at a '{difficulty}' difficulty level.
    Generate exactly {count} questions.
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=QuizResponse,
            temperature=0.3,
        ),
    )
    return QuizResponse.model_validate_json(response.text)

# ==========================================
# 3. VISUAL INTERFACE LAYER (Streamlit UI)
# ==========================================
st.set_page_config(page_title="AI Quiz Generator", page_icon="🎓", layout="centered")
st.title("🎓 Intelligent AI Quiz Generator")
st.caption("Powered by Gemini 2.5 Flash & Structured JSON Data Output Schemas")

# Sidebar Configuration Controls
st.sidebar.header("🔧 Quiz Configurations")
input_topic = st.sidebar.text_input("Enter Topic/Subject", placeholder="e.g., Python Data Structures")
input_diff = st.sidebar.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Advanced"])
input_count = st.sidebar.slider("Number of Questions", min_value=3, max_value=10, value=5)

# Session State Initialization (Keeps our data alive when clicking buttons)
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# Trigger Quiz Generation
if st.sidebar.button("✨ Generate Live Quiz", use_container_width=True):
    if not input_topic.strip():
        st.sidebar.error("Please enter a valid topic first!")
    else:
        with st.spinner("AI is crafting your structured quiz questions..."):
            try:
                # Reset states for a fresh quiz run
                st.session_state.quiz_data = generate_quiz(input_topic, input_diff, input_count)
                st.session_state.user_answers = {}
                st.session_state.submitted = False
            except Exception as e:
                st.error(f"Failed to generate quiz data safely. Error trace: {str(e)}")

# Render the Quiz Form to the Screen
if st.session_state.quiz_data:
    quiz = st.session_state.quiz_data
    st.subheader(f"📝 Quiz: {quiz.topic} ({quiz.difficulty} Level)")
    
    # We use a form layout so the screen doesn't refresh constantly when choosing answers
    with st.form("quiz_submission_form"):
        for i, q in enumerate(quiz.questions):
            st.markdown(f"**Q{i+1}: {q.question_text}**")
            
            # Render individual choice radio controls
            user_choice = st.radio(
                f"Select an option for Q{i+1}:",
                options=q.options,
                key=f"q_{i}",
                index=None, # No default pre-selected answer
                label_visibility="collapsed"
            )
            
            # Store whatever the user clicked into session memory
            if user_choice is not None:
                st.session_state.user_answers[i] = q.options.index(user_choice)
            
            st.markdown("---")
            
        submit_btn = st.form_submit_button("🏁 Submit Answers for Grading")

    # Evaluation Dashboard Calculation Logic
    if submit_btn or st.session_state.submitted:
        st.session_state.submitted = True
        st.success("📊 Evaluation Complete! See Results Below:")
        
        score = 0
        for i, q in enumerate(quiz.questions):
            user_ans = st.session_state.user_answers.get(i, None)
            correct_ans = q.correct_option_index
            
            st.markdown(f"#### Question {i+1}")
            st.write(q.question_text)
            
            if user_ans == correct_ans:
                st.info(f"✅ **Correct!** Your Answer: *{q.options[user_ans]}*")
                score += 1
            else:
                user_text = q.options[user_ans] if user_ans is not None else "Skipped"
                st.error(f"❌ **Incorrect.** Your Answer: *{user_text}* | Correct Answer: *{q.options[correct_ans]}*")
            
            # Display explanation text passed down strictly by the LLM
            st.caption(f"💡 *Explanation:* {q.explanation}")
            st.markdown("---")
            
        # Display Final Summary Analytics Cards
        st.metric(label="Final Score", value=f"{score} / {len(quiz.questions)}", delta=f"{int((score/len(quiz.questions))*100)}% Pass Rate")
