import streamlit as st
from openai import OpenAI
import dotenv
import os
from PIL import Image
from audio_recorder_streamlit import audio_recorder
import base64
from io import BytesIO

dotenv.load_dotenv()

# Function to query and stream the responses from the LLM
def stream_llm_response(client, model_params):
    response_message = ""
    for chunk in client.chat.completions.create(
        model=model_params.get("model", "gpt-4o"),
        messages=st.session_state.messages,
        temperature=model_params.get("temperature", 0.3),
        max_tokens=4096,
        stream=True,
    ):
        content = chunk.choices[0].delta.get("content", "")
        response_message += content
        yield content

    st.session_state.messages.append({
        "role": "assistant",
        "content": [{
            "type": "text",
            "text": response_message,
        }]
    })

# Function to convert file to base64
def get_image_base64(image_raw):
    buffered = BytesIO()
    image_raw.save(buffered, format=image_raw.format)
    img_byte = buffered.getvalue()

    return base64.b64encode(img_byte).decode("utf-8")

def main():
    # --- Page Config ---
    st.set_page_config(
        page_title="Super Assistant",
        page_icon="🤖",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    # Custom CSS Styling for the page
    st.markdown("""
        <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f0f4f8;
            color: #333;
        }
        h1 {
            color: #6ca395;
            text-align: center;
        }
        .stButton button {
            background-color: #6ca395;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 16px;
            border: none;
        }
        .stButton button:hover {
            background-color: #4f8f75;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- Header ---
    st.markdown("""<h1>🤖 <i>The Super Assistant</i> 💬</h1>""", unsafe_allow_html=True)

    # OpenAI API Key
    default_openai_api_key = os.getenv("OPENAI_API_KEY", "")
    openai_api_key = st.text_input(
        "Introduce your OpenAI API KEY (https://platform.openai.com/)", 
        value=default_openai_api_key, 
        type="password"
    )

    if not openai_api_key or "sk-" not in openai_api_key:
        st.warning("⬅️ Please introduce your OpenAI API key (make sure to have funds) to continue")
        return

    # Initialize OpenAI client
    client = OpenAI(api_key=openai_api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            for content in message["content"]:
                if content["type"] == "text":
                    st.markdown(content["text"])

    # Model options
    model = st.selectbox("Select a model:", [
        "gpt-4o",
        "gpt-4-turbo",
        "gpt-3.5-turbo",
    ], index=0)

    temperature = st.slider("Temperature", 0.0, 2.0, 0.3)

    model_params = {
        "model": model,
        "temperature": temperature,
    }

    # Reset conversation button
    if st.button("🗑️ Reset conversation"):
        st.session_state.messages.clear()

    # Chat input
    if prompt := st.chat_input("Hi! Ask me anything..."):
        st.session_state.messages.append({
            "role": "user",
            "content": [{
                "type": "text",
                "text": prompt,
            }]
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        # Placeholder for streaming response
        response_placeholder = st.empty()
        full_response = ""

        with st.chat_message("assistant"):
            for chunk in stream_llm_response(client, model_params):
                full_response += chunk
                response_placeholder.markdown(full_response)

        # Append full response to session state
        st.session_state.messages.append({
            "role": "assistant",
            "content": [{
                "type": "text",
                "text": full_response,
            }]
        })

if __name__ == "__main__":
    main()
