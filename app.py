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
css_lines = [
    "<style>",
    "@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');",
    "* { font-family: 'Plus Jakarta Sans', sans-serif; }",
    ".stApp { background: radial-gradient(circle at 10% 20%, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 1) 90%); color: #f1f5f9; }",
    "[data-testid='stSidebar'] { background: rgba(15, 23, 42, 0.95) !important; border-right: 1px solid rgba(255, 255, 255, 0.08) !important; backdrop-filter: blur(16px); }",
    ".header-card { background: linear-gradient(135deg, rgba(255, 255, 255, 0.06), rgba(255, 255, 255, 0.01)); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 20px; padding: 26px 30px; margin-bottom: 24px; box-shadow: 0 12px 36px 0 rgba(0, 0, 0, 0.45); }",
    ".badge { display: inline-flex; align-items: center; gap: 6px; padding: 6px 16px; border-radius: 9999px; font-size: 0.8rem; font-weight: 700; background: rgba(255, 75, 75, 0.15); color: #ff6b6b; border: 1px solid rgba(255, 75, 75, 0.35); margin-bottom: 14px; letter-spacing: 0.5px; }",
    ".stTextInput input { background: rgba(30, 41, 59, 0.85) !important; color: #ffffff !important; border: 1px solid rgba(255, 255, 255, 0.18) !important; border-radius: 14px !important; padding: 14px 20px !important; font-size: 1.05rem !important; height: 54px !important; transition: all 0.3s ease; }",
    ".stTextInput input:focus { border-color: #6366f1 !important; box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25) !important; }",
    "div[data-testid='stCustomComponentV1'] { display: flex; align-items: flex-end; height: 100%; justify-content: center; }",
    "div[data-testid='stCustomComponentV1'] button { background: #ffffff !important; color: #dc2626 !important; font-size: 1.75rem !important; height: 54px !important; width: 100% !important; min-width: 56px !important; border-radius: 14px !important; border: 2px solid #f1f5f9 !important; box-shadow: 0 6px 20px rgba(255, 255, 255, 0.2) !important; display: flex; justify-content: center; align-items: center; cursor: pointer; transition: all 0.25s ease-in-out !important; }",
    "div[data-testid='stCustomComponentV1'] button:hover { transform: translateY(-2px) scale(1.04) !important; background: #f8fafc !important; box-shadow: 0 8px 25px rgba(255, 255, 255, 0.4) !important; }",
    ".stButton>button { width: 100%; background: linear-gradient(135deg, #ff4b4b 0%, #dc2626 100%) !important; color: #ffffff !important; font-weight: 700 !important; font-size: 1.05rem !important; padding: 14px 24px !important; border-radius: 14px !important; border: none !important; cursor: pointer; transition: all 0.25s ease-in-out !important; box-shadow: 0 6px 22px rgba(220, 38, 38, 0.35); margin-top: 14px; }",
    ".stButton>button:hover { transform: translateY(-2px); box-shadow: 0 10px 28px rgba(220, 38, 38, 0.5) !important; }",
    ".result-box { background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 18px; padding: 24px 28px; backdrop-filter: blur(16px); line-height: 1.7; margin-top: 24px; margin-bottom: 20px; box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3); }",
    "</style>"
]
st.markdown("\n".join(css_lines), unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. साइडबार सेटअप (Bilingual)
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚡ **RK AI Studio**")
    st.caption("✨ *आपका पर्सनल AI / Your Personal AI*")
    st.markdown("---")

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
    st.info(
        "💡 **सुझाव / Pro-Tip:** Focus on one topic at a time so that you "
        "can understand it in depth/एक समय में एक ही टॉपिक पर फोकस करें "
        "ताकि आप गहराई से समझ सकें।"
    )

# ---------------------------------------------------------
# 4. मुख्य हेडर (AI Thinking & Learning Partner)
# ---------------------------------------------------------
header_lines = [
    "<div class='header-card'>",
    "    <div class='badge'>🚀 Powered by RK COACHING CENTRE</div>",
    "    <h1 style='margin: 0; font-size: 2.15rem; font-weight: 800; "
    "background: linear-gradient(90deg, #ffffff, #94a3b8); "
    "-webkit-background-clip: text; -webkit-text-fill-color: transparent;'>",
    "        RK AI Thinking & Learning Partner 🧠",
    "    </h1>",
    "    <p style='margin: 10px 0 0 0; color: #94a3b8; font-size: 1.05rem; line-height: 1.6;'>",
    "        Type or speak any topic, AI will explain it with simple explanations and real-world examples.<br>",
    "        <span style='font-size: 0.95rem; color: #64748b;'>(कोई भी टॉपिक लिखें या बोलें, AI उसे आसान भाषा, वास्तविक उदाहरणों और सही स्ट्रक्चर के साथ समझाएगा।)</span>",
    "    </p>",
    "</div>"
]
st.markdown("\n".join(header_lines), unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. इनपुट बार + माइक बटन
# ---------------------------------------------------------
audio_lang = "hi-IN" if "Hindi" in language else "en-US"

if "search_query" not in st.session_state:
    st.session_state.search_query = ""

col_text, col_mic = st.columns([10.5, 1.5], vertical_alignment="bottom")

with col_text:
    user_input = st.text_input(
        "📌 विषय (Topic) का नाम लिखें या माइक दबाएं:",
        value=st.session_state.search_query,
        placeholder="उदा. What is Computer?, Computer Memory (RAM/ROM)..."
    )

with col_mic:
    spoken_text = speech_to_text(
        language=audio_lang,
        start_prompt="🎙️",
        stop_prompt="⏹️",
        key="speech_input"
    )
    if spoken_text:
        st.session_state.search_query = spoken_text
        st.rerun()

# ---------------------------------------------------------
# 6. मुख्य सर्च बटन
# ---------------------------------------------------------
search_clicked = st.button("🔍 सर्च करें / Search")

# ---------------------------------------------------------
# 7. सर्च लॉजिक एवं आउटपुट जनरेशन
# ---------------------------------------------------------
active_topic = user_input.strip()

if search_clicked:
    if not active_topic:
        st.warning("⚠️ कृपया पहले कोई टॉपिक लिखें या बोलें / Please write or speak a topic first.")
    else:
        if "GEMINI_API_KEY" not in st.secrets:
            st.error("❌ 'GEMINI_API_KEY' नहीं मिली! कृपया Streamlit Secrets में अपनी API Key जोड़ें।")
        else:
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel("gemini-2.5-flash")

                if "Hindi" in language:
                    lang_rule = "उत्तर पूरी तरह से सरल और स्पष्ट हिंदी में दें। तकनीकी शब्दों को कोष्ठक में अंग्रेजी में लिख सकते हैं।"
                else:
                    lang_rule = "Provide the entire response clearly in English."

                if "Understand Concept" in mode:
                    goal_prompt = f"टॉपिक '{active_topic}' को बिल्कुल आसान तरीके से समझाएं। इसमें परिभाषा, कैसे काम करता है, एक दैनिक जीवन का उदाहरण और इसके मुख्य फायदे बताएं।"
                elif "Learning Roadmap" in mode:
                    goal_prompt = f"टॉपिक '{active_topic}' को शुरुआत से सीखने का पूरा स्टेप-बाय-स्टेप रोडमैप (Beginner से Advanced) तैयार करें।"
                else:
                    goal_prompt = f"टॉपिक '{active_topic}' पर 3 बहुविकल्पीय प्रश्न (MCQs) उत्तर सहित और 2 महत्वपूर्ण अभ्यास प्रश्न तैयार करें।"

                full_prompt = (
                    f"विषय: {active_topic}\n"
                    f"लक्ष्य: {goal_prompt}\n"
                    f"भाषा: {lang_rule}\n"
                    "फॉर्मेट: स्पष्ट सब-हेडिंग्स, बुलेट पॉइंट्स और आसान भाषा में उत्तर प्रस्तुत करें।"
                )

                with st.spinner("🔍 सर्च किया जा रहा है... कृपया प्रतीक्षा करें..."):
                    response = model.generate_content(full_prompt)

                    card_html = (
                        "<div class='
