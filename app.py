import streamlit as st
from PIL import Image
from transformers import pipeline

# ================== PAGE CONFIG ==================
st.set_page_config(page_title="LinguaWise AI", page_icon="🌍", layout="wide")

# ================== BRANDING ==================
logo = Image.open("logo.png")

st.markdown("""
    <style>
        .main {
            background-color: #F9FAFB;
        }
        .stApp header {
            background: linear-gradient(90deg, #4F46E5, #22C55E);
            padding: 5px;
        }
        .block-container {
            padding-top: 1rem;
        }
        .css-1d391kg, .css-18e3th9 {
            background-color: #EEF2FF !important; /* sidebar bg */
            color: #1E1E1E !important;
        }
    </style>
""", unsafe_allow_html=True)

# ================== TOP BAR ==================
col1, col2 = st.columns([1, 5])
with col1:
    st.image(logo, width=70)
with col2:
    st.markdown("<h1 style='color:#4F46E5;'>LinguaWise AI</h1>", unsafe_allow_html=True)
    st.markdown("### 🌍 Break Language Barriers with AI")

# ================== MENU ==================
menu = ["Home", "Features", "Pricing", "Contact", "Chatbot"]
choice = st.sidebar.radio("Navigate", menu)

# ================== HOME ==================
if choice == "Home":
    st.markdown("## 🚀 World Languages at Your Fingertips")
    st.write(
        "LinguaWise AI is your multilingual assistant that works across industries. "
        "Communicate effortlessly in **50+ languages** with AI-powered smart responses."
    )
    st.markdown("👉 [Try the Chatbot](#chatbot)")

# ================== FEATURES ==================
elif choice == "Features":
    st.header("✨ Key Features")
    st.write("- 🌍 **Multilingual Support**: 50+ global & Indic languages")
    st.write("- 🏢 **Domain Agnostic**: Works for any industry")
    st.write("- ⚡ **Fast & Real-time**: Instant replies")
    st.write("- 🔗 **Integrations**: WhatsApp, websites, CRMs")
    st.write("- 📊 **Analytics**: Usage insights & reports")

# ================== PRICING ==================
elif choice == "Pricing":
    st.header("💰 Pricing Plans")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Basic")
        st.metric("Price", "$0")
        st.write("✔ 1 chatbot\n✔ 2 languages\n✔ 500 chats/month")
        st.button("Choose Basic")

    with col2:
        st.subheader("Pro")
        st.metric("Price", "$49/mo")
        st.write("✔ Unlimited chats\n✔ 10 languages\n✔ Analytics dashboard")
        st.button("Choose Pro")

    with col3:
        st.subheader("Enterprise")
        st.metric("Price", "Custom")
        st.write("✔ Unlimited everything\n✔ API access\n✔ Dedicated support")
        st.button("Contact Sales")

# ================== CONTACT ==================
elif choice == "Contact":
    st.header("📩 Contact Us")
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    msg = st.text_area("Message")
    if st.button("Send"):
        st.success("✅ Thanks! We'll get back to you soon.")

# ================== CHATBOT ==================
elif choice == "Chatbot":
    st.title("💬 LinguaWise Multilingual Chatbot")

    # --- Load Models ---
    @st.cache_resource
    def load_models():
        translator = pipeline("translation", model="facebook/mbart-large-50-many-to-many-mmt")
        generator = pipeline("text-generation", model="aswinprasath31/guvi-gpt2-finetuned")
        detector = pipeline("text-classification", model="papluca/xlm-roberta-base-language-detection")
        return translator, generator, detector

    with st.spinner("Initializing AI models, please wait..."):
        translator, generator, detector = load_models()

    MODEL_LANG_MAP = {
        "ar": "ar_AR", "cs": "cs_CZ", "de": "de_DE", "en": "en_XX", "es": "es_XX",
        "fr": "fr_XX", "gu": "gu_IN", "hi": "hi_IN", "it": "it_IT", "ja": "ja_XX",
        "ko": "ko_KR", "pt": "pt_XX", "ru": "ru_RU", "ta": "ta_IN", "te": "te_IN",
        "zh": "zh_CN"
    }

    # --- Chat History ---
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! 🌍 How can I assist you today?"}
        ]

    # Display past chats
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # --- Response Logic ---
    def get_bot_response(user_input):
        detection_result = detector(user_input)
        detected_lang_code = detection_result[0]['label']
        src_lang_code = MODEL_LANG_MAP.get(detected_lang_code, "en_XX")

        if src_lang_code == "en_XX":
            english_query = user_input
        else:
            translated_to_en = translator(user_input, src_lang=src_lang_code, tgt_lang="en_XX")
            english_query = translated_to_en[0]['translation_text']

        prompt = f"Answer the following question in a clear, helpful way: {english_query}"
        gpt_response = generator(prompt, max_length=200, num_return_sequences=1)
        english_response = gpt_response[0]['generated_text']

        if src_lang_code == "en_XX":
            return english_response
        else:
            translated_to_orig = translator(english_response, src_lang="en_XX", tgt_lang=src_lang_code)
            return translated_to_orig[0]['translation_text']

    # --- Input Box ---
    if user_input := st.chat_input("Ask me anything..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_bot_response(user_input)
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

# ================== FOOTER ==================
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:grey'>© 2025 <b>LinguaWise AI</b> | All Rights Reserved</div>",
    unsafe_allow_html=True,
)
