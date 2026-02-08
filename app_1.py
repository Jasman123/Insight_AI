import streamlit as st

# Page config
st.set_page_config(
    page_title="Internal Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)

# ---- Sidebar ----
with st.sidebar:
    st.markdown("## 🤖 LLM-powered Assistant")
    st.write("Professional AI support for internal knowledge management.")
    st.divider()
    st.selectbox("LLMs Models", options=["🧠 Gemini", "🤖  GPT-3.5", "🧬 Claude"], index=0)
    st.info("""This assistant uses multiple LLMs for internal knowledge management. ' \
    'The data is securely managed and not shared with external parties.
            and the most recent update file is from 2024-05-15, including 123 documents """, icon="ℹ️")

# ---- Main ----
st.markdown("## Internal Knowledge Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello 👋 How can I assist you today?"}
    ]

# Chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
prompt = st.chat_input("Type your message here...")

if prompt:
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response (placeholder)
    with st.chat_message("assistant"):
        response = "Thank you for your message. Our team is processing your request."
        st.markdown(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
