import streamlit as st
from transformers import pipeline
from PIL import Image

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="LinguaWise AI",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ LOAD LOGO ------------------
logo = Image.open("logo.png")

# ------------------ CUSTOM CSS ------------------
st.markdown("""
    <style>
        .stApp {
            background-color: #F9FAFB;
            color: #1F2937;
            font-family: "Inter", sans-serif;
        }

        /* USER bubble */
        .stChatMessage[data-testid="stChatMessage-user"] {
            background: #E5E7EB;
            color: #111827;
            border-radius: 16px 16px 0px 16px;
            padding: 10px 14px;
            margin: 6px 0;
            text-align: right;
            max-width: 70%;
            margin-left: auto;
        }

        /* BOT bubble */
        .stChatMessage[data-testid="stChatMessage-assistant"] {
            background: #4F46E5;
            color: white;
            border-radius: 16px 16px 16px 0px;
            padding: 10px 14px;
            margin: 6px 0;
            text-align: left;
            max-width: 70%;
            margin-right: auto;
        }

        /* Input box */
        .stTextInput>div>div>input {
            border: 2px solid #4F46E5;
            border-radius: 30px;
            padding: 12px 20px;
            font-size: 16px;
        }

        /* Send button */
        .stButton>button {
            background-color: #4F46E5;
            color: white;
            border-radius: 50%;
            border: none;
            width: 45px;
            height: 45px;
            font-size: 18px;
            margin-top: 5px;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #4338CA;
            transform: translateY(-2px) scale(1.05);
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #EEF2FF;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------ LOAD MODELS ------------------
@st.cache_resource
def load_models():
    translator = pipeline("translation", model="facebook/mbart-large-50-many-to-many-mmt")
    generator = pipeline("text-generation", model="aswinprasath31/guvi-gpt2-finetuned")
    detector = pipeline("text-classification", model="papluca/xlm-roberta-base-language-detection")
    return translator, generator, detector

with st.spinner("Loading AI models..."):
    translator, generator, detector = load_models()

# Language mapping
MODEL_LANG_MAP = {
    "ar": "ar_AR", "cs": "cs_CZ", "de": "de_DE", "en": "en_XX", "es": "es_XX",
    "fr": "fr_XX", "gu": "gu_IN", "hi": "hi_IN", "it": "it_IT", "ja": "ja_XX",
    "ko": "ko_KR", "ml": "ml_IN", "mr": "mr_IN", "pt": "pt_XX", "ta": "ta_IN",
    "te": "te_IN", "zh": "zh_CN"
}

# ------------------ CHATBOT LOGIC ------------------
def get_bot_response(user_input):
    if len(user_input.split()) < 3:
        return "That's a broad topic! Could you please ask a more specific question?"

    detection_result = detector(user_input)
    detected_lang_code = detection_result[0]['label']
    src_lang_code = MODEL_LANG_MAP.get(detected_lang_code, "en_XX")

    if src_lang_code == "en_XX":
        english_query = user_input
    else:
        translated = translator(user_input, src_lang=src_lang_code, tgt_lang="en_XX")
        english_query = translated[0]['translation_text']

    prompt = f"Answer the following question in a helpful and clear manner: {english_query}"
    gpt_response = generator(prompt, max_length=200, num_return_sequences=1)
    english_response = gpt_response[0]['generated_text']

    if src_lang_code == "en_XX":
        return english_response
    else:
        translated_back = translator(english_response, src_lang="en_XX", tgt_lang=src_lang_code)
        return translated_back[0]['translation_text']

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.image(logo, width=100)
    st.title("LinguaWise AI 🌍")
    st.info("Your multilingual AI assistant for every domain.")
    st.markdown("**Key Features:**")
    st.markdown("- 🌐 Multilingual support\n- 🤖 GPT-2 fine-tuned answers\n- ⚡ Real-time chat")
    st.markdown("---")
    st.header("Navigation")
    page = st.radio("Go to:", ["Chatbot", "Features", "Pricing", "Contact"])

# ------------------ PAGES ------------------
if page == "Chatbot":
    st.title("💬 LinguaWise Chatbot")
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you today?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    col1, col2 = st.columns([10,1])
    with col1:
        user_input = st.chat_input("Type your message here...")
    with col2:
        send_btn = st.button("➤")

    if user_input or send_btn:
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = get_bot_response(user_input)
                st.markdown(response)

            st.session_state.messages.append({"role": "assistant", "content": response})

elif page == "Features":
    st.title("✨ Features")
    st.write("""
    - 🌍 **Multilingual Chatbot** – supports 20+ languages  
    - 🧠 **AI-powered answers** – fine-tuned GPT-2 model  
    - ⚡ **Instant responses** – real-time chat  
    - 🏢 **For all domains** – education, business, customer support, etc.  
    """)

elif page == "Pricing":
    st.title("💰 Pricing Plans")
    st.write("Choose the right plan for your needs:")
    st.markdown("""
    | Plan       | Features                           | Price   |
    |------------|------------------------------------|---------|
    | **Basic**  | 5 languages, limited usage         | Free    |
    | **Pro**    | 20 languages, priority support     | $19/mo  |
    | **Enterprise** | Unlimited usage, custom models | Contact |
    """)

elif page == "Contact":
    st.title("📩 Contact Us")
    st.write("We’d love to hear from you. Fill out the form below:")
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_area("Message")
    if st.button("Send Message"):
        st.success("Thank you! We'll get back to you soon.")

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: grey;'>© 2025 LinguaWise AI | Developed by Aswinprasath V</div>",
    unsafe_allow_html=True
)
