import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text

# ---------------------------------------------------------
# 1. पेज सेटअप (Meta Config)
# ---------------------------------------------------------
st.set_page_config(
    page_title="RK AI Studio | Smart Learning Hub",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. अल्ट्रा-मॉडर्न डार्क UI और कस्टम CSS
# ---------------------------------------------------------
css_rules = [
    "<style>",
    "@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');",
    "* { font-family: 'Plus Jakarta Sans', sans-serif; }",
    ".stApp { background: radial-gradient(circle at 10% 20%, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 1) 90%); color: #f1f5f9; }",
    "[data-testid='stSidebar'] { background: rgba(15, 23, 42, 0.95) !important; border-right: 1px solid rgba(255, 255, 255, 0.08) !important; backdrop-filter: blur(16px); }",
    ".header-card { background: linear-gradient(135deg, rgba(255, 255, 255, 0.06), rgba(255, 255, 255, 0.01)); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 20px; padding: 26px 30px; margin-bottom: 24px; box-shadow: 0 12px 36px 0 rgba(0, 0, 0, 0.45); }",
    ".badge { display: inline-flex; align-items: center; gap: 6px; padding: 6px 16px; border-radius: 9999px; font-size: 0.8rem; font-weight: 70
