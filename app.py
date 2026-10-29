import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text

# पेज कॉन्फिगरेशन
st.set_page_config(page_title="RK COACHING CENTRE - Smart Learning", page_icon="🎓", layout="wide")

# कस्टम स्टाइलिंग
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #ff4b4b; color: white; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# साइडबार
with st.sidebar:
    st.title("🎓 RK COACHING CENTRE")
    st.write("आपका पर्सनल AI मेंटर")
    api_key = st.text_input("अपनी Gemini API Key डालें:", type="password")
    
    st.markdown("---")
    st.markdown("### आपको क्या करना है?")
    mode = st.radio("चुनें:", ["💡 टॉपिक समझें (Concept)", "🛣️ रोडमैप (Roadmap)", "📝 टेस्ट लें (Quiz)"])
    st.info("💡 केवल एक टॉपिक शुरू करने से आपकी तैयारी बेहतर होगी!")

# मुख्य हेडिंग
st.title("⚡ AI Learning & Study Dashboard")
st.write("कोई भी टॉपिक लिखें या बोलें, AI उसे आसान भाषा और रियल-लाइफ उदाहरण के साथ समझाएगा।")

# वॉइस / माइक इनपुट
st.write("🎤 **बोलकर टॉपिक बताएं (माइक पर क्लिक करें):**")
spoken_text = speech_to_text(language='hi-IN', start_prompt="रिकॉर्डिंग शुरू करें", stop_prompt="रोकें", key='speech_input')

# यदि बोलकर इनपुट मिला तो उसे डिफ़ॉल्ट बनाएं, नहीं तो खाली रखें
default_topic = spoken_text if spoken_text else ""

user_input = st.text_input("विषय (Topic) का नाम लिखें:", value=default_topic, placeholder="उदा: What is Cloud Computing, Excel Formulas...")

# कंटेंट जनरेशन बटन
if st.button("कंटेंट जनरेट करें 🚀"):
    if not api_key:
        st.warning("कृपया पहले साइडबार में अपनी Gemini API Key डालें!")
    elif not user_input.strip():
        st.warning("कृपया कोई टॉपिक लिखें या माइक से बोलें!")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-3.5-flash")

            if mode == "💡 टॉपिक समझें (Concept)":
                prompt = f"आप एक बेहतरीन शिक्षक हैं। कृपया इस टॉपिक '{user_input}' को आसान हिंदी में समझाइए। इसमें शामिल करें: 1. आसान परिभाषा, 2. रियल-लाइफ उदाहरण, 3. महत्वपूर्ण बातें।"
            elif mode == "🛣️ रोडमैप (Roadmap)":
                prompt = f"छात्र के लिए '{user_input}' सीखने के लिए स्टेप-बाय-स्टेप 30 दिन का आसान रोडमैप तैयार करें।"
            else:
                prompt = f"विषय '{user_input}' पर आधारित 5 महत्वपूर्ण बहुविकल्पीय प्रश्न (MCQs) बनाएं, जिनके 4 विकल्प हों और अंत में सही उत्तर व व्याख्या भी दें।"

            with st.spinner("AI आपके लिए कंटेंट तैयार कर रहा है..."):
                response = model.generate_content(prompt)

            st.success("तैयार है!")
            st.markdown("---")
            st.markdown(response.text)

        except Exception as e:
            st.error(f"कुछ समस्या आई: {e}")
