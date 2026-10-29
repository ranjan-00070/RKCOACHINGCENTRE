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
        transition: all 0.3s ease;
    }
    .stTextInput input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25) !important;
    }

    /* बटन स्टाइलिंग */
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
# 3. साइडबार सेटअप (Bilingual Hindi + English)
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚡ **RK AI Studio**")
    st.caption("✨ *आपका पर्सनल AI मेंटर / Your Personal AI Mentor*")
    st.markdown("---")

    api_key = st.secrets["GEMINI_API_KEY"]

    # भाषा का चयन (अर्थ आइकन व दोनों भाषाओं के साथ)
    language = st.radio(
        "🌍 **भाषा चुनें / Select Language:**",
        ["हिंदी (Hindi)", "English"],
        index=0
    )

    st.markdown("---")

    # मोड चयन (हिंदी + अंग्रेजी दोनों के साथ)
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
    st.info("💡 **सुझाव / Pro-Tip:** एक समय में एक ही टॉपिक पर फोकस करें ताकि आप गहराई से समझ सकें। / Focus on one topic at a time for deeper mastery.")

# ---------------------------------------------------------
# 4. मुख्य हेडर (Bilingual)
# ---------------------------------------------------------
st.markdown("""
<div class="header-card">
    <div class="badge">🚀 Powered by Gemini 2.5 Flash</div>
    <h1 style="margin: 0; font-size: 2.1rem; font-weight: 800; background: linear-gradient(90deg, #ffffff, #94a3b8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        AI Thinking & Mentorship Hub 🧠
    </h1>
    <p style="margin: 10px 0 0 0; color: #94a3b8; font-size: 1.05rem;">
        कोई भी टॉपिक लिखें या बोलें, AI उसे आसान भाषा, वास्तविक उदाहरणों और सही स्ट्रक्चर के साथ समझाएगा।<br>
        <span style="font-size: 0.95rem; color: #64748b;">(Type or speak any topic, AI will explain it with simple explanations and real-world examples.)</span>
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. इनपुट एवं माइक सेक्शन
# ---------------------------------------------------------
audio_lang = "hi-IN" if language == "हिंदी (Hindi)" else "en-US"

col_mic, col_gap = st.columns([1, 2])
with col_mic:
    spoken_text = speech_to_text(
        language=audio_lang,
        start_prompt="🎙️ बोलकर सर्च करें / Tap to Speak",
        stop_prompt="⏹️ रिकॉर्डिंग रोकें / Stop Recording",
        key="speech_input"
    )

default_topic = spoken_text if spoken_text else ""

# कंप्यूटर और टेक से जुड़े वास्तविक उदाहरणों वाला प्लेसहोल्डर
user_input = st.text_input(
    "📌 विषय (Topic) का नाम लिखें / Enter Topic Name:",
    value=default_topic,
    placeholder="उदा. What is Computer?, Computer Memory (RAM/ROM), Python Loops, Database Basics..."
)

# ---------------------------------------------------------
# 6. जनरेशन एवं आउटपुट
# ---------------------------------------------------------
if st.button("🚀 AI सर्च करें / Generate with AI"):
    if not user_input.strip():
        st.warning("⚠️ कृपया पहले कोई टॉपिक लिखें या माइक से बोलें! / Please enter a topic or use the mic.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash")

            if "💡 टॉपिक समझें" in mode:
                prompt = (
                    f"आप एक उत्कृष्ट कंप्यूटर और अकादमिक शिक्षक हैं। कृपया इस विषय को बहुत ही आसान भाषा, "
                    f"स्पष्ट पॉइंट्स और दैनिक/व्यावहारिक जीवन के रियल-लाइफ उदाहरणों (Real-life Examples) के साथ समझाएं: {user_input}"
                )
            elif "🛣️ सीखने का रोडमैप" in mode:
                prompt = (
                    f"कृपया इस विषय को बेसिक से एडवांस तक सीखने के लिए एक व्यावहारिक, चरण-दर-चरण "
                    f"(Step-by-Step) समयबद्ध रोडमैप (Learning Roadmap) तैयार करें: {user_input}"
                )
            else:
                prompt = (
                    f"कृपया '{user_input}' पर आधारित 5 महत्वपूर्ण परीक्षा-उपयोगी अभ्यास प्रश्न (Quiz/MCQs) तैयार करें, "
                    f"जिनमें सही उत्तर और उनके स्पष्ट कारण (Explanation) भी शामिल हों।"
                )

            # भाषा निर्देश
            if language == "हिंदी (Hindi)":
                final_prompt = f"{prompt}\n\nकृपया पूरा उत्तर सरल, सहज हिंदी में दें और तकनीकी शब्दों (Technical Terms) को कोष्ठक (brackets) में अंग्रेजी में भी लिखें ताकि समझना आसान हो।"
            else:
                final_prompt = f"{prompt}\n\nPlease provide the complete response clearly, structurally, and professionally in English."

            with st.spinner("⚡ AI कंटेंट तैयार कर रहा है... / AI is generating your content..."):
                response = model.generate_content(final_prompt)

            st.success("✅ उत्तर तैयार है! / Response is ready!")
            
            # रिस्पॉन्स को साफ़-सुथरे कार्ड बॉक्स में प्रदर्शित करना
            st.markdown(f'<div class="result-box">{response.text}</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ समस्या आई / Error encountered: {e}")
