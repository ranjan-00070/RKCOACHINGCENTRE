import streamlit as st
import google.generativeai as genai
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
    spoken
