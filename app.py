import streamlit as st
from PIL import Image

# ================== PAGE CONFIG ==================
st.set_page_config(page_title="LinguaWise AI", page_icon="🌍", layout="wide")

# ================== BRANDING ==================
try:
    logo = Image.open("logo.png")
    st.sidebar.image(logo, width=120)
except:
    st.sidebar.markdown("### 🌍 LinguaWise AI")

st.sidebar.title("Navigation")
menu = ["Home", "Features", "Pricing", "Contact"]
choice = st.sidebar.radio("Go to", menu)

# ================== HOME ==================
if choice == "Home":
    st.markdown("<h1 style='color:#4F46E5;'>🌍 LinguaWise AI</h1>", unsafe_allow_html=True)
    st.subheader("Break Language Barriers with AI 🤖")
    st.write(
        "LinguaWise AI is your multilingual assistant that adapts to **any industry**. "
        "Communicate effortlessly in **50+ languages** with AI-powered smart responses."
    )
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=250)

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

# ================== FOOTER ==================
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:grey'>© 2025 <b>LinguaWise AI</b> | All Rights Reserved</div>",
    unsafe_allow_html=True,
)

# ================== FLOATING CHATBOT POPUP ==================
chatbot_url = "https://aswinprasath31-guvi-multilingual-chatbot.hf.space"  # Hugging Face space

chatbot_code = f"""
    <style>
        /* Floating button */
        .chatbot-button {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: #4F46E5;
            color: white;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            text-align: center;
            font-size: 30px;
            cursor: pointer;
            z-index: 9999;
            box-shadow: 0px 4px 6px rgba(0,0,0,0.3);
        }}
        /* Chatbot popup */
        .chatbot-popup {{
            display: none;
            position: fixed;
            bottom: 90px;
            right: 20px;
            width: 350px;
            height: 500px;
            border: 2px solid #4F46E5;
            border-radius: 12px;
            overflow: hidden;
            z-index: 9998;
            background: white;
        }}
    </style>

    <div class="chatbot-button" onclick="toggleChatbot()">💬</div>
    <div id="chatbot" class="chatbot-popup">
        <iframe src="{chatbot_url}" width="100%" height="100%" frameborder="0"></iframe>
    </div>

    <script>
        function toggleChatbot() {{
            var x = document.getElementById("chatbot");
            if (x.style.display === "none" || x.style.display === "") {{
                x.style.display = "block";
            }} else {{
                x.style.display = "none";
            }}
        }}
    </script>
"""

st.markdown(chatbot_code, unsafe_allow_html=True)
