import os
import tempfile
import streamlit as st
from dotenv import load_dotenv
from graph_model import build_graph
from uuid import uuid4
from gtts import gTTS
import logging
from datetime import datetime

import concurrent.futures
import time

REQUEST_TIMEOUT_SECONDS = 60
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, f"error_{datetime.now().strftime('%Y-%m-%d')}.txt"),
    level=logging.ERROR,
    format="%(asctime)s | %(levelname)s | %(message)s",
)



load_dotenv()
st.set_page_config(page_title="PDF Chatbot", page_icon="🤖", layout="centered")
st.title("📄 RAG EPIC Project by Jasman")

@st.cache_resource
def init_graph():
    return build_graph()

graph = init_graph()

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "language" not in st.session_state:
    st.session_state.language = "en"

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


def invoke_with_timeout(graph, payload, config, timeout=30):
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(graph.invoke, payload, config)
        try:
            return future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            raise TimeoutError("LLM request timed out")



error_message = {}
try:
    user_input = st.chat_input("Ask something about the PDF...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.spinner("Thinking..."):
            result = invoke_with_timeout(
                graph=graph,
                payload={"messages": st.session_state.messages},
                config={"configurable": {"thread_id": st.session_state.thread_id}},
                timeout=REQUEST_TIMEOUT_SECONDS
            )


            assistant_reply = result["messages"][-1].content

        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
        with st.chat_message("assistant"):
            st.markdown(assistant_reply)
        if st.session_state.language == "en":
            assistant_reply = st.session_state.messages[-1]["content"]
            tts = gTTS(text=assistant_reply, lang="en")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                tts.save(tmp_file.name)
                audio_path = tmp_file.name
            with open(audio_path, "rb") as audio_file:
                st.audio(audio_file.read(), format="audio/mp3")
            os.remove(audio_path)

except TimeoutError as e:
    st.error("⏱️ Request timed out. The model took too long to respond. Please try again.")
    logging.error(
        f"Thread ID: {st.session_state.get('thread_id')} | TIMEOUT | {str(e)}"
    )
    
except Exception as e:
    st.error(f"An error occurred: please try again later or LLMs models.")
    error_text = str(e)
    logging.error(
        f"Thread ID: {st.session_state.get('thread_id')} | Error: {error_text}",
        exc_info=True
    )

        