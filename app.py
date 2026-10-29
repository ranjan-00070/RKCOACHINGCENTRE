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
# 2. अल्ट्रा-मॉडर्न एडेप्टिव CSS (Light & Dark Both Supported)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* --- कलर वैरिएबल्स (डिफ़ॉल्ट: Dark Theme) --- */
    :root {
        --app-bg: radial-gradient(circle at 10% 20%, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 1) 90%);
        --text-main: #f8fafc;
        --text-sub: #94a3b8;
        --text-muted: #64748b;
        --card-bg: rgba(30, 41, 59, 0.6);
        --card-border: rgba(255, 255, 255, 0.12);
        --input-bg: rgba(30, 41, 59, 0.85);
        --input-text: #ffffff;
        --input-border: rgba(255, 255, 255, 0.18);
        --mic-bg: #ffffff;
        --mic-border: #e2e8f0;
        --mic-shadow: rgba(255, 255, 255
