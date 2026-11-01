import streamlit as st
from google import genai
from streamlit_mic_recorder import speech_to_text

# 1. पेज सेटअप
st.set_page_config(
    page_title="RK AI Studio | Smart Learning Hub",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. साइडबार सेटअप
with st.sidebar:
    st.title("⚡ RK AI Studio")
    st.caption("✨ आपका पर्सनल AI / Your Personal AI")
    st.divider()

    language = st.radio(
        "🌍 भाषा चुनें / Select Language:",
        ["हिंदी (Hindi)", "English"],
        index=0
    )

    st.divider()
    st.write("🎯 **अपना लक्ष्य चुनें / Choose Your Learning Goal:**")
    mode = st.radio(
        label="मोड चुनें:",
        options=[
            "💡 टॉपिक समझें / Understand Concept (In Detail)",
            "🛣️ सीखने का रोडमैप / Learning Roadmap (Step-by-Step)",
            "📝 टेस्ट और सवाल / Quiz & Practice Questions"
        ],
        label_visibility="collapsed"
    )

    st.divider()
    st.info(
        "💡 **सुझाव / Pro-Tip:** Focus on one topic at a time so that you "
        "can understand it in depth / एक समय में एक ही टॉपिक पर फोकस करें "
        "ताकि आप गहराई से समझ सकें।"
    )

# 3. मुख्य हेडर
st.caption("🚀 POWERED BY RK COACHING CENTRE")
st.title("RK AI Thinking & Learning Partner 🧠")
st.write(
    "Type or speak any topic, AI will explain it with simple "
    "explanations and real-world examples."
)
st.caption(
    "(कोई भी टॉपिक लिखें या बोलें, AI उसे आसान भाषा, "
    "वास्तविक उदाहरणों और सही स्ट्रक्चर के साथ समझाएगा।)"
)
st.divider()

# 4. इनपुट बार और माइक
audio_lang = "hi-IN" if "Hindi" in language else "en-US"

if "search_query" not in st.session_state:
    st.session_state.search_query = ""

col_text, col_mic = st.columns([10, 2], vertical_alignment="bottom")

with col_text:
    user_input = st.text_input(
        "📌 विषय (Topic) का नाम लिखें या माइक दबाएं:",
        value=st.session_state.search_query,
        placeholder="उदा. What is Computer?, Computer Memory (RAM/ROM)..."
    )

with col_mic:
    spoken_text = speech_to_text(
        language=audio_lang,
        start_prompt="🎙️ बोलें",
        stop_prompt="⏹️ रुकें",
        key="speech_input"
    )
    if spoken_text:
        st.session_state.search_query = spoken_text
        st.rerun()

# 5. मुख्य सर्च बटन
search_clicked = st.button(
    "🔍 सर्च करें / Search",
    type="primary",
    use_container_width=True
)

# 6. सर्च लॉजिक एवं आउटपुट जनरेशन
active_topic = user_input.strip()

if search_clicked:
    if not active_topic:
        st.warning(
            "⚠️ कृपया पहले कोई टॉपिक लिखें या बोलें / "
            "Please write or speak a topic first."
        )
    elif "GEMINI_API_KEY" not in st.secrets:
        st.error(
            "❌ 'GEMINI_API_KEY' नहीं मिली! "
            "कृपया Streamlit Secrets में अपनी API Key जोड़ें।"
        )
    else:
        try:
            # नया तेज़ GenAI क्लाइंट
            client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

            if "Hindi" in language:
                lang_rule = (
                    "उत्तर पूरी तरह से सरल और स्पष्ट हिंदी में दें। "
                    "तकनीकी शब्दों को कोष्ठक में अंग्रेजी में लिख सकते हैं।"
                )
            else:
                lang_rule = "Provide the entire response clearly in English."

            if "Understand Concept" in mode:
                goal_prompt = (
                    f"टॉपिक '{active_topic}' को बिल्कुल आसान तरीके से समझाएं। "
                    "इसमें परिभाषा, कैसे काम करता है, एक दैनिक जीवन का उदाहरण "
                    "और इसके मुख्य फायदे बताएं।"
                )
            elif "Learning Roadmap" in mode:
                goal_prompt = (
                    f"टॉपिक '{active_topic}' को शुरुआत से सीखने का पूरा "
                    "स्टेप-बाय-स्टेप रोडमैप (Beginner से Advanced) तैयार करें।"
                )
            else:
                goal_prompt = (
                    f"टॉपिक '{active_topic}' पर 3 बहुविकल्पीय प्रश्न (MCQs) "
                    "उत्तर सहित और 2 महत्वपूर्ण अभ्यास प्रश्न तैयार करें।"
                )

            full_prompt = (
                f"विषय: {active_topic}\n"
                f"लक्ष्य: {goal_prompt}\n"
                f"भाषा: {lang_rule}\n"
                "फॉर्मेट: स्पष्ट सब-हेडिंग्स, बुलेट पॉइंट्स और आसान भाषा में उत्तर प्रस्तुत करें।"
            )

            with st.spinner("🔍 सर्च किया जा रहा है... कृपया प्रतीक्षा करें..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=full_prompt,
                )

                with st.container(border=True):
                    st.subheader(f"📌 परिणाम: {active_topic}")
                    st.markdown(response.text)

        except Exception as e:
            st.error(f"❌ सर्च करने में समस्या आई: {e}")
