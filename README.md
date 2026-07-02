# 🎓 Intelligent AI Quiz Generator with Strict JSON Schema Enforcement

A web application built using Python that dynamically generates structured multiple-choice quizzes on any academic or technical topic. The application uses state-of-the-art Generative AI combined with client-side runtime validation schemas to completely eliminate unpredictable LLM outputs.

---

## 🚀 Engineering Highlights
* **Zero Chaotic AI Text Outputs:** Uses **Pydantic Data Schemas** tied directly to the LLM generation configurations (`response_schema`), forcing the AI to strictly output valid JSON variables.
* **100% Deterministic Parsing:** The application completely bypasses fragile string parsing or regex searching by ingesting direct, structured structural objects (`QuizResponse`).
* **Session State Management:** Built using specialized browser memory contexts to track user input options, evaluation metrics, and score grading flags across screen redraws.
* **Cloud Security Architecture:** Built to safely inject api tokens through encrypted environment parameters (`os.environ.get`), preventing critical credential leaks on open-source platforms.

---

## 🏗️ System Workflow

```text
┌─────────────────┐       Topic & Parameters      ┌──────────────────┐
│   Streamlit     │ ────────────────────────────> │  Google Gemini   │
│ User Dashboard  │                               │   2.5 Flash API  │
│ (Frontend Tier) │ <──────────────────────────── │ (Inference Tier) │
└─────────────────┘       Strict JSON Payload     └──────────────────┘
         │                         │
         │ (State Validation)      │ (Strict Schema Binding)
         ▼                         ▼
┌────────────────────────────────────────────────────────────────────┐
│                  Pydantic Object Integrity Layer                    │
│   Ensures exact compliance for: Questions, Choices, Keys, Contexts │
└────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ The Tech Stack

* **Language Platform:** `Python 3.11+`
* **Core Inference Orchestrator:** `google-genai` (SDK Core Client)
* **LLM Core Blueprint Engine:** `gemini-2.5-flash`
* **Runtime Data Validation Framework:** `Pydantic v2`
* **User Experience (UX) Architecture:** `Streamlit Web Engine`

---

## 📂 Repository Layout

```text
ai-quiz-generator/
│
├── app.py                # Main Application Driver (Orchestration & UX Elements)
├── requirements.txt      # Explicit project software version dependencies
└── README.md             # Complete structural documentation dossier
```

---

## 💻 Local Setup & Execution Deployment

### 1. Clone the Codebase
```bash
git clone https://github.com
cd ai-quiz-generator
```

### 2. Configure Virtual Environment Dependencies
```bash
# Initialize isolated Python environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install strictly verified project packages
pip install -r requirements.txt
```

### 3. Start the Active Server Locally
```bash
streamlit run app.py
```
Your local server environment dashboard will spin up instantly at **`http://localhost:8501`**.

---

## 🧪 Expected JSON Structural Blueprint

Below is an abstract example of the clean data contract enforced between the AI Engine and our local runtime loop:

```json
{
  "topic": "Python Data Structures",
  "difficulty": "Intermediate",
  "questions": [
    {
      "question_text": "Which of the following data structures in Python is inherently unordered?",
      "options": ["List", "Tuple", "Set", "Dictionary"],
      "correct_option_index": 2,
      "explanation": "Sets are built using hash tables and are unordered collections of unique data elements."
    }
  ]
}
```
# gen-ai-quiz-generator
