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
# 2. अल्ट्रा-मॉडर्न डार्क UI और कस्टम CSS (Syntax Safe)
# ---------------------------------------------------------
custom_css = (
    "<style>\n"
    "@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');\n"
    "* { font-family: 'Plus Jakarta Sans', sans-serif; }\n"
    ".stApp {\n"
    "    background: radial-gradient(circle at 10% 20%, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 1) 90%);\n"
    "    color: #f1f5f9;\n"
    "}\n"
    "[data-testid='stSidebar'] {\n"
    "    background: rgba(15, 23, 42, 0.95) !important;\n"
    "    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;\n"
    "    backdrop-filter: blur(16px);\n"
    "}\n"
    ".header-card {\n"
    "    background: linear-gradient(135deg, rgba(255, 255, 255, 0.06), rgba(255, 255, 255, 0.01));\n"
    "    border: 1px solid rgba(255, 255, 255, 0.12);\n"
    "    border-radius: 20px;\n"
    "    padding: 26px 30px;\n"
    "    margin-bottom: 24px;\n"
    "    box-shadow: 0 12px 36px 0 rgba(0, 0, 0, 0.45);\n"
    "}\n"
    ".badge {\n"
    "    display: inline-flex;\n"
    "    align-items: center;\n"
    "    gap: 6px;\n"
    "    padding: 6px 16px;\n"
    "    border-radius: 9999px;\n"
    "    font-size: 0.8rem;\n"
    "    font-weight: 700;\n"
    "    background: rgba(255, 75, 75, 0.15);\n"
    "    color: #ff6b6b;\n"
    "    border: 1px solid rgba(255, 75, 75, 0.35);\n"
    "    margin-bottom: 14px;\n"
    "    letter-spacing: 0.5px;\n"
    "}\n"
    ".stTextInput input {\n"
    "    background: rgba(30, 41, 59, 0.85) !important;\n"
    "    color: #ffffff !important;\n"
    "    border: 1px solid rgba(255, 255, 255, 0.18) !important;\n"
    "    border-radius: 14px !important;\n"
    "    padding: 14px 20px !important;\n"
    "    font-size: 1.05rem !important;\n"
    "    height: 54px !important;\n"
    "    transition: all 0.3s ease;\n"
    "}\n"
    ".stTextInput input:focus {\n"
    "    border-color: #6366f1 !important;\n"
    "    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25
