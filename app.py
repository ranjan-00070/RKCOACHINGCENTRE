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
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* मुख्य बैकग्राउंड */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 1) 90%);
        color: #f1f5f9;
    }

    /* साइडबार कंटेनर */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.9);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
    }

    /* हेडर कार्ड */
    .header-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.01));
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 18px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.35);
    }

    .badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 700;
        background: rgba(255, 75, 75, 0.15);
        color: #ff6b6b;
        border: 1px solid rgba(255, 75, 75, 0.3);
        margin-bottom: 12px;
        letter-spacing: 0.6px;
    }

    /* इनपुट बॉक्स */
    .stTextInput input {
        background: rgba(30, 41, 59, 0.8) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        font-size: 1.05rem !important;
        height: 52px !important;
        transition: all 0.3s ease;
    }
    .stTextInput input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25) !important;
    }

    /* माइक बटन की वाइट बॉक्स स्टाइलिंग */
    div[data-testid="stCustomComponentV1"] {
        display: flex;
        align-items: flex-end;
        height: 100%;
        justify-content: center;
    }
    div[data-testid="stCustomComponentV1"] button {
        background: #ffffff !important;
        color: #dc2626 !important;
        font-size: 1.75rem !important;
        height: 52px !important;
        width: 100% !important;
        min-width: 54px !important;
        border-radius: 14px !important;
        border: 2px solid #f1f5f9 !important;
        box-shadow: 0 6px 20px rgba(255, 255, 255, 0.25) !important;
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
        transition: all 0.25s ease-in-out !important;
    }
    div[data-testid="stCustomComponentV1"] button:hover {
        transform: translateY(-2px) scale(1.05) !important;
        background: #f8fafc !important;
        box-shadow: 0 8px 25px rgba(255, 255, 255, 0.45) !important;
    }

    /* मुख्य सर्च बटन */
    .stButton>button {
        width: 100%;
        background: linear-
