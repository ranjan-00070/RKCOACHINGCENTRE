import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text
from gtts import gTTS
from io import BytesIO
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
    st.write(" आपका  Personal  AI ")
    api_key = st.secrets["GEMINI_API_KEY"]
    language = st.sidebar.radio("भाषा चुनें / Select Language:", ["हिंदी (Hindi)", "English"])
    st.markdown("---")
    st.markdown("### Choose Your Topic:")
    mode = st.radio("आपको क्या करना हैं?", ["💡 समझें (in brief)", "🛣️ प्लान बनाएं (Make Plans)", "📝 सवाल बनाएं (Make Questions)"])
    st.info("💡 केवल एक टॉपिक शुरू करने से आपकी तैयारी बेहतर होगी!")

# मुख्य हेडिंग
st.title("🧠 𝗔𝗜 𝗧𝗵𝗶𝗻𝗸𝗶𝗻𝗴 💬 𝗙𝗼𝗿 𝗬𝗼𝘂𝗿 𝗕𝗲𝘁𝘁𝗲𝗿 𝗟𝗲𝗮𝗿𝗻𝗶𝗻𝗴 🚀")
st.write("कोई भी Topic लिखें या बोलें, AI उसे Easy Language और Real-Life Example के साथ समझाएगा।")

# ---------------------------------------------------------
# मुख्य हेडिंग एवं माइक / इनपुट
# ---------------------------------------------------------


# साइडबार में चुनी भाषा के आधार पर माइक की भाषा सेट करना
audio_lang = "hi-IN" if language == "हिंदी (Hindi)" else "en-US"

spoken_text = speech_to_text(
    language=audio_lang, 
    start_prompt="🎙️ बोलकर Search 🔎 करें (Search By Mic)", 
    key="speech"
)

# यदि बोलकर इनपुट मिला तो उसे डिफ़ॉल्ट बनाएं, नहीं तो खाली रखें
default_topic = spoken_text if spoken_text else ""

user_input = st.text_input("विषय (Topic) का नाम लिखें", value=default_topic)

# ---------------------------------------------------------
# कंटेंट जनरेशन बटन
# ---------------------------------------------------------
if st.button("अब Search 🔎 करें"):
    if not user_input.strip():
        st.warning("कृपया कोई टॉपिक लिखें या माइक से बोलें!")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-3.5-flash")

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
# Audio Player Code
        try:
            tts_lang = 'hi' if language == "हिंदी (Hindi)" else 'en'
            sound_file = BytesIO()
            tts = gTTS(text=response.text, lang=tts_lang, slow=False)
            tts.write_to_fp(sound_file)
            st.audio(sound_file, format='audio/mp3')
        except Exception as e:
            st.warning("Audio generate nahi ho paya.")
        except Exception as e:
            st.error(f"कुछ समस्या आई: {e}")
