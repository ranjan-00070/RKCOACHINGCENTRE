import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text

# ---------------------------------------------------------
# 1. पेज सेटअप (Full-Featured Meta Config)
# ---------------------------------------------------------
st.set_page_config(
    page_title="RK AI Studio | Next-Gen Learning Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. अल्ट्रा-मॉडर्न डार्क UI/UX और कस्टम CSS (SaaS Level)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* डार्क नियॉन ग्रेडिएंट बैकग्राउंड */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 1) 90%);
        color: #f1f5f9;
    }

    /* साइडबार कंटेनर */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.85);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
    }

    /* प्रीमियम हेडर कार्ड */
    .header-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.04), rgba(255, 255, 255, 0.01));
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }

    .badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 700;
        background: rgba(255, 75, 75, 0.15);
        color: #ff6b6b;
        border: 1px solid rgba(255, 75, 75, 0.3);
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    /* इनपुट बॉक्स */
    .stTextInput input {
        background: rgba(30, 41, 59, 0.7) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        font-size: 1.05rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    .stTextInput input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25) !important;
        background: rgba(30, 41, 59, 0.95) !important;
    }

    /* ग्रेडिएंट बटन */
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

    /* आउटपुट रिस्पॉन्स कार्ड */
    .result-box {
        background: rgba(30, 41, 59, 0.5);
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
# 3. साइडबार सेटअप (Sidebar Controls)
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚡ **RK AI Studio**")
    st.caption("✨ *Intelligent Learning & Coaching System*")
    st.markdown("---")

    api_key = st.secrets["GEMINI_API_KEY"]

    # भाषा का चयन
    language = st.radio(
        "🌐 **भाषा चुनें / Select Language:**",
        ["हिंदी (Hindi)", "English"],
        index=0
    )

    st.markdown("---")

    # मोड चयन
    st.markdown("🎯 **सीखने का उद्देश्य (Choose Mode):**")
    mode = st.radio(
        label="मोड चुनें",
        options=[
            "💡 समझें (Concept in Detail)",
            "🗺️ रोडमैप (Learning Roadmap)",
            "📝 टेस्ट और अभ्यास (Quiz & Practice)"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.info("💡 **प्रो-टिप:** एक समय में एक ही टॉपिक पर फोकस करें ताकि आप गहराई से समझ सकें।")

# ---------------------------------------------------------
# 4. मुख्य डैशबोर्ड हेडर
# ---------------------------------------------------------
st.markdown("""
<div class="header-card">
    <div class="badge">🚀 Powered by Gemini 2.5 Flash</div>
    <h1 style="margin: 0; font-size: 2.2rem; font-weight: 800; background: linear-gradient(90deg, #ffffff, #94a3b8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        AI Thinking & Mentorship Hub
    </h1>
    <p style="margin: 10px 0 0 0; color: #94a3b8; font-size: 1.05rem;">
        किसी भी टॉपिक को टाइप करें या बोलें—AI आपको आसान भाषा, रोडमैप और उदाहरणों के साथ गाइड करेगा।
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. इनपुट और माइक सेक्शन
# ---------------------------------------------------------
audio_lang = "hi-IN" if language == "हिंदी (Hindi)" else "en-US"

col_mic, col_gap = st.columns([1, 2])
with col_mic:
    spoken_text = speech_to_text(
        language=audio_lang,
        start_prompt="🎙️ बोलकर सर्च करें (Speak by Mic)",
        stop_prompt="⏹️ रिकॉर्डिंग रोकें",
        key="speech_input"
    )

default_topic = spoken_text if spoken_text else ""

user_input = st.text_input(
    "📌 अपना टॉपिक यहाँ दर्ज करें:",
    value=default_topic,
    placeholder="उदा. Python Basics, Accounting Principles, Cloud Computing..."
)

# ---------------------------------------------------------
# 6. जनरेशन और आउटपुट प्रोसेसिंग
# ---------------------------------------------------------
if st.button("🚀 AI विश्लेषण शुरू करें (Generate Insights)"):
    if not user_input.strip():
        st.warning("⚠️ कृपया पहले कोई टॉपिक लिखें या माइक से बोलें!")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash")

            if mode == "💡 समझें (Concept in Detail)":
                prompt = (
                    f"आप एक कुशल शिक्षक हैं। कृपया इस विषय को बहुत ही आसान भाषा, रोचक शैली और दैनिक जीवन के "
                    f"उदाहरणों के साथ विस्तार से समझाएं: {user_input}"
                )
            elif mode == "🗺️ रोडमैप (Learning Roadmap)":
                prompt = (
                    f"कृपया इस विषय को शून्य से शिखर तक सीखने के लिए एक व्यावहारिक, चरण-दर-चरण "
                    f"(Step-by-Step) समयबद्ध रोडमैप तैयार करें: {user_input}"
                )
            else:
                prompt = (
                    f"कृपया '{user_input}' पर आधारित 5 महत्वपूर्ण परीक्षा-उपयोगी अभ्यास प्रश्न (Quiz) तैयार करें, "
                    f"जिनमें सही उत्तर और विस्तृत व्याख्या भी शामिल हो।"
                )

            if language == "हिंदी (Hindi)":
                final_prompt = f"{prompt}\n\nकृपया उत्तर पूरी तरह से शुद्ध, सहज और स्पष्ट हिंदी में ही लिखें।"
            else:
                final_prompt = f"{prompt}\n\nPlease provide the entire response clearly and professionally in English."

            with st.spinner("⚡ AI कंटेंट तैयार कर रहा है... कृपया प्रतीक्षा करें..."):
                response = model.generate_content(final_prompt)

            st.success("✅ विश्लेषण सफलता से पूर्ण हुआ!")
            
            # रिस्पॉन्स को क्लीन कार्ड बॉक्स में प्रदर्शित करना
            st.markdown(f'<div class="result-box">{response.text}</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ समस्या आई: {e}")
