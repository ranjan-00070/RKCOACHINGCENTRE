import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text

# पेज कॉन्फिगरेशन
st.set_page_config(page_title="RK Coaching Centre - Smart Learning", page_icon="🎓", layout="wide")

# कस्टम स्टाइलिंग
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #ff4b4b; color: white; font-weight: bold; }
</style>
""", unsafe_allow_html_true=True)

# साइडबार
with st.sidebar:
    st.title("🎓 RK Coaching Centre")
    st.write("आपका पर्सनल AI मेंटर")
    api_key = st.text_input("अपनी Gemini API Key डालें:", type="password")
    
    st.markdown("---")
    st.markdown("### आपको क्या करना है?")
    mode = st.radio("चुनें:", ["💡 टॉपिक समझें (Concept)", "🛣️ रोडमैप (Roadmap)", "📝 टेस्ट लें (Quiz)"])
    st.info("💡 केवल एक टॉपिक शुरू करने से आपकी तैयारी बेहतर होगी!")

# मुख्य हेडिंग
st.title("⚡ AI Learning & Study Dashboard")
st.write("कोई भी टॉपिक लिखें या बोलें, AI उसे आसान भाषा और रियल")
