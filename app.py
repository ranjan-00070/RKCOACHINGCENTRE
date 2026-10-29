import streamlit as st
from google import genai

# पेज की सेटिंग
st.set_page_config(page_title="RK Coaching Centre - Smart Learning", page_icon="🎓", layout="wide")

# कस्टम स्टाइलिंग (डार्क और प्रीमियम लुक)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #4F46E5; color: white; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# साइडबार (Sidebar)
with st.sidebar:
    st.title("🎓 RK Coaching Centre")
    st.write("आपका पर्सनल AI मेंटर")
    api_key = st.text_input("अपनी Gemini API Key डालें:", type="password")
    
    st.markdown("---")
    mode = st.radio("आपको क्या करना है?", ["📚 टॉपिक समझें (Concept)", "🗺️ स्टडी प्लान (Roadmap)", "📝 टेस्ट लें (Quiz)"])
    st.info("💡 रोज़ाना एक टॉपिक पूरा करने से आपकी स्किल बेहतर होगी।")

# मुख्य स्क्रीन (Main Dashboard)
st.header("⚡ AI Learning & Study Dashboard")
st.write("कोई भी टॉपिक लिखें, AI उसे आसान भाषा और रियल लाइफ उदाहरण के साथ समझाएगा।")

user_input = st.text_input("विषय (Topic) का नाम लिखें:", placeholder="उदा: What is Cloud Computing, Excel Formulas, Stock Market basics...")

if st.button("कंटेंट जनरेट करें 🚀"):
    if not api_key:
        st.warning("कृपया पहले साइडबार में अपनी Gemini API Key डालें!")
    elif not user_input:
        st.warning("कृपया कोई टॉपिक तो लिखिए!")
    else:
        with st.spinner("AI आपके लिए नोट्स तैयार कर रहा है..."):
            try:
                client = genai.Client(api_key=api_key)
                if mode == "📚 टॉपिक समझें (Concept)":
                    prompt = f"विषय: {user_input}। इसे बहुत सरल हिंदी में समझाएं। इसमें शामिल करें: 1. आसान परिभाषा, 2. रोज़मर्रा की ज़िंदगी का एक उदाहरण (Analogy), 3. महत्वपूर्ण बुलेट पॉइंट्स, 4. याद रखने की एक ज़रूरी टिप।"
                elif mode == "🗺️ स्टडी प्लान (Roadmap)":
                    prompt = f"विषय: {user_input}। इसे शुरू से सीखने के लिए एक 7-दिन का स्टेप-बाय-स्टेप स्टडी रोडमैप तैयार करें। हर दिन क्या पढ़ना है साफ़ लिखें।"
                else:
                    prompt = f"विषय: {user_input}। इस टॉपिक पर 3 महत्वपूर्ण बहुविकल्पीय प्रश्न (MCQs) बनाएं, जिसमें 4 विकल्प हों और नीचे सही उत्तर का स्पष्टीकरण भी दें।"
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                st.success("तैयार है!")
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"कुछ समस्या आई: {e}")
