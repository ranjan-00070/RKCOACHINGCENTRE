import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text

# पेज कॉन्फिगरेशन
st.set_page_config(page_title="RK AI Studio - Smart Learning", page_icon="🤖", layout="wide")

# कस्टम स्टाइलिंग
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #ff4b4b; color: white; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# साइडबार
with st.sidebar:
    st.title("🤖 RK AI Studio")
    st.write("आपका पर्सनल AI मेंटर")
    api_key = st.secrets["GEMINI_API_KEY"]
    language = st.sidebar.radio("भाषा चुनें / Select Language", ["हिंदी (Hindi)", "English"])
    st.markdown("---")
    st.markdown("### आपको क्या करना है?")
    mode = st.radio("चुनें:", ["💡 टॉपिक समझें (Concept)", "🛣️ रोडमैप (Roadmap)", "📝 टेस्ट लें (Quiz)"])
    st.info("💡 केवल एक टॉपिक शुरू करने से आपकी तैयारी बेहतर होगी!")

# मुख्य हेडिंग
st.title("⚡ AI Learning & Study Dashboard")
st.write("कोई भी टॉपिक लिखें या बोलें, AI उसे आसान भाषा और रियल-लाइफ उदाहरण के साथ समझाएगा।")

# ---------------------------------------------------------
# मुख्य हेडिंग एवं माइक / इनपुट
# ---------------------------------------------------------


# साइडबार में चुनी भाषा के आधार पर माइक की भाषा सेट करना
audio_lang = "hi-IN" if language == "हिंदी (Hindi)" else "en-US"

spoken_text = speech_to_text(
    language=audio_lang, 
    start_prompt="🎙️ बोलकर टॉपिक बताएं (माइक पर क्लिक करें)", 
    key="speech"
)

# यदि बोलकर इनपुट मिला तो उसे डिफ़ॉल्ट बनाएं, नहीं तो खाली रखें
default_topic = spoken_text if spoken_text else ""

user_input = st.text_input("विषय (Topic) का नाम लिखें", value=default_topic)

# ---------------------------------------------------------
# कंटेंट जनरेशन बटन
# ---------------------------------------------------------
if st.button("कंटेंट जनरेट करें 🚀"):
    if not user_input.strip():
        st.warning("कृपया कोई टॉपिक लिखें या माइक से बोलें!")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5pro")

            if mode == "💡 टॉपिक समझें (Concept)":
                prompt = f"आप एक बेहतरीन शिक्षक हैं। कृपया इस टॉपिक को बहुत आसान तरीके से समझाएं: {user_input}"
            elif mode == "🎯 रोडमैप (Roadmap)":
                prompt = f"कृपया इस टॉपिक को सीखने के लिए एक पूरा स्टेप-बाय-स्टेप रोडमैप तैयार करें: {user_input}"
            else:
                prompt = f"कृपया '{user_input}' पर आधारित 5 महत्वपूर्ण क्विज़/टेस्ट सवाल और उनके जवाब दें।"

            # भाषा के अनुसार Gemini को निर्देश
            if language == "हिंदी (Hindi)":
                final_prompt = f"{prompt}\n\nकृपया पूरा उत्तर सरल और स्पष्ट हिंदी में दें।"
            else:
                final_prompt = f"{prompt}\n\nPlease provide the complete response clearly in English."

            with st.spinner("AI आपके लिए कंटेंट तैयार कर रहा है..."):
                response = model.generate_content(final_prompt)

            st.success("तैयार है!")
            st.markdown(response.text)

        except Exception as e:
            st.error(f"कुछ समस्या आई: {e}")
