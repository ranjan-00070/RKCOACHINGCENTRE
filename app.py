import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text

# पेज कॉन्फ़िगरेशन
st.set_page_config(
    page_title="RK AI Studio | Smart Learning Hub",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# प्रोफेशनल कस्टम CSS स्टाइलिंग (Glassmorphism & Gradient Effects)
st.markdown("""
<style>
    /* मुख्य बैकग्राउंड और फॉन्ट */
    .stApp {
        background: radial-gradient(circle at top left, #161b22, #0d1117);
        color: #e6edf3;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* साइडबार स्टाइलिंग */
    [data-testid="stSidebar"] {
        background-color: #11161d;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* इनपुट बॉक्स स्टाइलिंग */
    .stTextInput input {
        background-color: #161b22;
        color: #ffffff;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 12px 16px;
        font-size: 1rem;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .stTextInput input:focus {
        border-color: #58a6ff;
        box-shadow: 0 0 0 2px rgba(88, 166, 255, 0.2);
    }

    /* प्रीमियम ग्रेडिएंट बटन */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #ff4b4b, #e03131);
        color: #ffffff;
        font-weight: 600;
        letter-spacing: 0.5px;
        font-size: 1rem;
        padding: 0.65rem 1.25rem;
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 14px rgba(255, 75, 75, 0.35);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 75, 75, 0.45);
        color: #ffffff;
    }
    .stButton>button:active {
        transform: translateY(0);
    }

    /* रिस्पॉन्स कार्ड बॉक्स */
    .response-card {
        background: rgba(22, 27, 34, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
        line-height: 1.6;
        backdrop-filter: blur(8px);
    }

    /* टैग्स और हेडर बैज */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        background: rgba(88, 166, 255, 0.15);
        color: #58a6ff;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# साइडबार सेटअप
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚡ **RK AI Studio**")
    st.caption("✨ *Your AI Mentor & Smart Tutor*")
    st.markdown("---")

    api_key = st.secrets["GEMINI_API_KEY"]

    # भाषा चयन (अर्थ आइकन के साथ)
    language = st.radio(
        "🌍 **भाषा चुनें / Select Language:**",
        ["हिंदी (Hindi)", "English"],
        index=0
    )

    st.markdown("---")

    # मोड चयन (सुव्यवस्थित आइकन्स के साथ)
    st.markdown("🎯 **अपना लक्ष्य चुनें (Choose Mode):**")
    mode = st.radio(
        label="ऑप्शन चुनें:",
        options=[
            "💡 समझें (Concept in Detail)",
            "🗺️ रोडमैप (Learning Roadmap)",
            "📝 टेस्ट और सवाल (Quiz & Practice)"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.info("💡 **सुझाव:** एक समय में एक विषय पर ध्यान देने से आपकी समझ और तैयारी अधिक मजबूत होगी!")

# ---------------------------------------------------------
# मुख्य हेडर और इंटरफेस
# ---------------------------------------------------------
st.markdown('<span class="badge">Next-Gen Education Engine</span>', unsafe_allow_html=True)
st.title("🧠 AI Learning & Thinking Dashboard")
st.markdown(
    "किसी भी विषय को टाइप करें या माइक से बोलें—AI उसे **सरल भाषा, व्यावहारिक उदाहरणों** और व्यवस्थित संरचना के साथ प्रस्तुत करेगा।"
)
st.write("")

# माइक सेटअप (चुनी गई भाषा के अनुसार)
audio_lang = "hi-IN" if language == "हिंदी (Hindi)" else "en-US"

col_mic, col_space = st.columns([1, 2])
with col_mic:
    spoken_text = speech_to_text(
        language=audio_lang,
        start_prompt="🎙️ बोलकर खोजें (Tap to Speak)",
        stop_prompt="⏹️ सुनना बंद करें",
        key="speech_input"
    )

# यदि माइक से आवाज़ इनपुट मिले तो उसे टेक्स्ट बॉक्स में भरें
default_topic = spoken_text if spoken_text else ""

user_input = st.text_input(
    "📌 विषय (Topic) का नाम लिखें:",
    value=default_topic,
    placeholder="उदा. Cloud Computing, Photosynthesis, Stock Market Basics..."
)

# ---------------------------------------------------------
# जनरेशन एवं आउटपुट
# ---------------------------------------------------------
if st.button("🚀 विश्लेषण शुरू करें (Generate with AI)"):
    if not user_input.strip():
        st.warning("⚠️ कृपया पहले कोई विषय टाइप करें या माइक से बोलें।")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash")

            # मोड के आधार पर प्रॉम्प्ट
            if mode == "💡 समझें (Concept in Detail)":
                prompt = (
                    f"आप एक कुशल शिक्षक हैं। कृपया इस विषय को बहुत ही सरल, रोचक और वास्तविक जीवन (Real-Life) "
                    f"के उदाहरणों के साथ विस्तार से समझाएँ: {user_input}"
                )
            elif mode == "🗺️ रोडमैप (Learning Roadmap)":
                prompt = (
                    f"कृपया इस विषय में महारत हासिल करने के लिए चरण-दर-चरण (Step-by-Step) समय-आधारित "
                    f"रोडमैप तैयार करें: {user_input}"
                )
            else:
                prompt = (
                    f"कृपया '{user_input}' पर आधारित 5 परीक्षा-उपयोगी अभ्यास प्रश्न (Quiz/Questions) "
                    f"उनके स्पष्ट उत्तरों और व्याख्या सहित तैयार करें।"
                )

            # भाषा निर्देश
            if language == "हिंदी (Hindi)":
                final_prompt = f"{prompt}\n\nकृपया उत्तर पूरी तरह से शुद्ध, सहज और स्पष्ट हिंदी में लिखें।"
            else:
                final_prompt = f"{prompt}\n\nPlease provide the entire response clearly and professionally in English."

            with st.spinner("⚡ AI आपके लिए सामग्री तैयार कर रहा है..."):
                response = model.generate_content(final_prompt)

            st.success("✅ विश्लेषण पूर्ण हुआ!")
            
            # रिस्पॉन्स को साफ़-सुथरे कार्ड में दिखाना
            st.markdown(f'<div class="response-card">{response.text}</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ तकनीकी समस्या आई: {e}")
