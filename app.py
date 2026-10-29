import streamlit as st
import google.generativeai as genai

# पेज कॉन्फ़िगरेशन
st.set_page_config(page_title="RK AI Studio - Smart Learning", page_icon="⚡", layout="wide")

# कस्टम स्टाइलिंग
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #ff4b4b; color: white; }
</style>
""", unsafe_allow_html=True)

# साइडबार
with st.sidebar:
    st.title("⚡ RK AI Studio")
    st.write("✨ **आपका Personal AI**")
    api_key = st.secrets["GEMINI_API_KEY"]
    language = st.sidebar.radio("🌐 Select Language / भाषा चुनें:", ["हिंदी (Hindi)", "English"])
    st.markdown("---")
    st.markdown("### Choose Your Topic:")
    mode = st.radio("आपको क्या करना है, चुनें:", ["💡 टॉपिक समझें (Concept)", "🛣️ रोडमैप (Roadmap)", "📝 टेस्ट / क्विज़ (Quiz)"])
    st.info("💡 केवल एक टॉपिक शुरू करने से आपकी तैयारी बेहतर होगी!")

# मुख्य हेडिंग
st.title("⚡ AI Thinking For Your Better Learning")
st.write("कोई भी Topic लिखें, AI उसे Easy Language और Real-Life Examples के साथ समझाएगा।")

# टेक्स्ट इनपुट बॉक्स
user_input = st.text_input("विषय (Topic) का नाम लिखें:")

# कंटेंट जनरेशन बटन
if st.button("✨ AI Search करें"):
    if not user_input.strip():
        st.warning("कृपया कोई टॉपिक लिखें।")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash")

            if mode == "💡 टॉपिक समझें (Concept)":
                prompt = f"आप एक बेहतरीन शिक्षक हैं। कृपया इस टॉपिक को बहुत आसान हिंदी में और रियल-लाइफ उदाहरण देकर विस्तार से समझाएं: {user_input}"
            elif mode == "🛣️ रोडमैप (Roadmap)":
                prompt = f"कृपया इस टॉपिक को सीखने के लिए एक पूरा स्टेप-बाय-स्टेप रोडमैप तैयार करें: {user_input}"
            else:
                prompt = f"कृपया '{user_input}' पर आधारित 5 महत्वपूर्ण क्विज/टेस्ट सवाल उत्तर सहित तैयार करें।"

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
