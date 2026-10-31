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
st.markdown("""
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

    /* माइक बटन की नई वाइट बॉक्स स्टाइलिंग (बड़ा साइज और क्लीन लुक) */
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

    /* मुख्य AI सर्च बटन */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #ff4b4b 0%, #dc2626 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        padding: 14px 24px !important;
        border-radius: 12px !important;
        border: none !important;
        cursor: pointer;
        transition: all 0.25s ease-in-out !important;
        box-shadow: 0 6px 20px rgba(220, 38, 38, 0.35);
        margin-top: 12px;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(220, 38, 38, 0.5) !important;
    }

    /* रिस्पॉन्स कार्ड */
    .result-box {
        background: rgba(30, 41, 59, 0.55);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(16px);
        line-height: 1.7;
        margin-top: 20px;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.25);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. साइडबार सेटअप (Bilingual)
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚡ **RK AI Studio**")
    st.caption("✨ *आपका पर्सनल AI / Your Personal AI*")
    st.markdown("---")

    api_key = st.secrets["GEMINI_API_KEY"]

    language = st.radio(
        "🌍 **भाषा चुनें / Select Language:**",
        ["हिंदी (Hindi)", "English"],
        index=0
    )

    st.markdown("---")

    st.markdown("🎯 **अपना लक्ष्य चुनें / Choose Your Learning Goal:**")
    mode = st.radio(
        label="मोड चुनें:",
        options=[
            "💡 टॉपिक समझें / Understand Concept (In Detail)",
            "🛣️ सीखने का रोडमैप / Learning Roadmap (Step-by-Step)",
            "📝 टेस्ट और सवाल / Quiz & Practice Questions"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.info("💡 **सुझाव / Pro-Tip:** एक समय में एक ही टॉपिक पर फोकस करें ताकि आप गहराई से समझ सकें।")

# ---------------------------------------------------------
# 4. मुख्य हेडर (AI Thinking & Learning Partner)
# ---------------------------------------------------------
st.markdown("""
<div class="header-card">
    <div class="badge">🚀 Powered by Gemini 1.5 Flash</div>
    <h1 style="margin: 0; font-size: 2.1rem; font-weight: 800; background: linear-gradient(90deg, #ffffff, #94a3b8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        AI Thinking & Learning Partner 🧠
    </h1>
    <p style="margin: 10px 0 0 0; color: #94a3b8; font-size: 1.05rem;">
        कोई भी टॉपिक लिखें या बोलें, AI उसे आसान भाषा, वास्तविक उदाहरणों और सही स्ट्रक्चर के साथ समझाएगा।<br>
        <span style="font-size: 0.95rem; color: #64748b;">(Type or speak any topic, AI will explain it with simple explanations and real-world examples.)</span>
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. इनपुट बार + बड़ा वाइट बॉक्स माइक बटन
# ---------------------------------------------------------
audio_lang = "hi-IN" if language == "हिंदी (Hindi)" else "en-US"

if "topic_input" not in st.session_state:
    st.session_state.topic_input = ""

# इनपुट बॉक्स और माइक बटन का ग्रिड लेआउट
col_text, col_mic = st.columns([10.5, 1.5], vertical_alignment="bottom")

with col_text:
    user_input = st.text_input(
        "📌 विषय (Topic) का नाम लिखें या माइक दबाएं:",
        value=st.session_state.topic_input,
        placeholder="उदा. What is Computer?, Computer Memory (RAM/ROM), Python Loops, Database Basics..."
    )

with col_mic:
    # व्हाइट बॉक्स में बड़ा माइक आइकॉन
    spoken_text = speech_to_text(
        language=audio_lang,
        start_prompt="🎙️",
        stop_prompt="⏹️",
        key="speech_input"
    )
    if spoken_text:
        st.session_state.topic_input = spoken_text
        st.rerun()

# ---------------------------------------------------------
# 6. मुख्य AI सर्च बटन
# ---------------------------------------------------------
search_clicked = st.button("🚀 AI सर्च करें / Generate with AI")

# ---------------------------------------------------------
# 7. AI जनरेशन एवं आउटपुट
# ---------------------------------------------------------
active_topic = user_input.strip()
