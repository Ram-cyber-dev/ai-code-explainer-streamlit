import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Page setup
st.set_page_config(
    page_title="Code Explainer AI",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Code Explainer AI")
st.caption("Paste code → get simple explanation, line-by-line breakdown, and improvements.")

# Load .env for local development
load_dotenv()

# Get API key (Streamlit Cloud or local .env)
api_key = None
try:
    api_key = st.secrets.get("GEMINI_API_KEY")
except Exception:
    pass

if not api_key:
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Missing GEMINI_API_KEY. Add it to .env (local) or Streamlit secrets (cloud).")
    st.stop()

# Gemini client
client = genai.Client(api_key=api_key)
MODEL = "gemini-2.5-flash"

# UI inputs
code_lang = st.selectbox(
    "Language",
    ["Python", "JavaScript", "TypeScript", "Java", "C++", "Other"],
)

code = st.text_area(
    "Paste your code here",
    height=260,
    placeholder="def add(a, b):\n    return a + b"
)

tone = st.selectbox(
    "Explanation style",
    ["Beginner-friendly", "Intermediate", "Super simple (like I'm 12)"],
)

# Action
if st.button("Explain Code", type="primary"):
    if not code.strip():
        st.warning("Please paste some code first.")
        st.stop()

    with st.spinner("Thinking..."):
        prompt = f"""
You are a senior developer and teacher.
Explain the following {code_lang} code in {tone} style.

Return output in this exact structure:

1) What this code does (2–4 sentences)
2) Line-by-line explanation (bullet points, reference line numbers)
3) 2–3 improvements (bullet points)
4) Any risks or bugs (if any)

CODE:
{code}
"""
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )
            st.subheader("✅ Explanation")
            st.write(response.text)
        except Exception as e:
            st.error(f"Gemini API error: {e}")
