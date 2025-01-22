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
         model=model_params["model"] if "model" in model_params else "gpt-4o",
         messages=st.session_state.messages,
         temperature=model_params["temperature"] if "temperature" in model_params else 0.3,
         max_tokens=4096,
         stream=True,
    ):
        response_message += chunk.choices[0].delta.content if chunk.choices[0].delta.content else ""
        yield chunk.choices[0].delta.content if chunk.choices[0].delta.content else ""

    st.session_state.messages.append({
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": response_message,
            }
        ]
    })

# Function to convert file to base64
def get_image_base64(image_raw):
    buffered = BytesIO()
    image_raw.save(buffered, format=image_raw.format)
    img_byte = buffered.getvalue()

    return base64.b64encode(img_byte).decode('utf-8')

def main():
    # --- Page Config ---
    st.set_page_config(
        page_title="super assistant",
        page_icon="🤖",
        layout="centered",
        initial_sidebar_state="collapsed",  # Sidebar is removed, as all content is now on the main page.
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
        .stTextInput input {
            border-radius: 5px;
            border: 2px solid #6ca395;
        }
        .stTextInput input:focus {
            border-color: #4f8f75;
        }
        .stSlider input {
            background-color: #6ca395;
        }
        .stAlert {
            background-color: #fff3e0;
            border-left: 5px solid #ff8c00;
            color: #ff8c00;
        }
        .stSelectbox, .stFileUploader, .stCheckbox {
            border: 2px solid #6ca395;
            border-radius: 5px;
        }
        .stSelectbox select, .stFileUploader input, .stCheckbox input {
            color: #6ca395;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- Header ---
    st.markdown("""<h1>🤖 <i>The Super Assistant</i> 💬</h1>""", unsafe_allow_html=True)

    # Main content
    default_openai_api_key = os.getenv("OPENAI_API_KEY") if os.getenv("OPENAI_API_KEY") is not None else ""
    openai_api_key = st.text_input("Introduce your OpenAI API KEY(https://platform.openai.com/)", value=default_openai_api_key, type="password")

    if not (openai_api_key == "" or openai_api_key is None or "sk-" not in openai_api_key):
        st.divider()
    
    if openai_api_key == "" or openai_api_key is None or "sk-" not in openai_api_key:
        st.write("#")
        st.warning("⬅️ Please introduce your OpenAI API(make sure to have funds) to continue")
    else:
        client = OpenAI(api_key=openai_api_key)
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Displaying previous messages if there are any
        # Displaying previous messages if there are any
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                for content in message["content"]:
                    if isinstance(content, dict):  # Ensure content is a dictionary
                        if content["type"] == "text":
                            st.write(content["text"])
                        elif content["type"] == "image_url":
                            st.image(content["image_url"]["url"])
                    elif isinstance(content, str):  # Handle cases where content is a string
                        st.write(content)


        # Model options and inputs
        model = st.selectbox("Select a model:", [
            "gpt-4o",
            "gpt-4-turbo",
            "gpt-3.5-turbo",
            "gpt-4o-2014-05-13",
            "gpt-4-37k",
        ], index=0)

        model_temp = st.slider("Temperature", min_value=0.0, max_value=2.0, value=0.3, step=0.3)

        audio_response = st.toggle("Audio response", value=False)
        if audio_response:
            cols = st.columns(2)
            with cols[0]:
                tts_voice = st.selectbox("Select a voice:", ["alloy", "echo", "fable", "onyx", "nova", "shimmer"])
            with cols[1]:
                tts_model = st.selectbox("Select a model:", ["tts-1", "tts-1-hd"], index=1)

        model_params = {
            "model": model,
            "temperature": model_temp,
        }

        def reset_conversation():
            if "messages" in st.session_state and len(st.session_state.messages) > 0:
                st.session_state.pop("messages", None)

        st.button(
            "🗑️ Reset conversation",
            on_click=reset_conversation,
        )

        st.divider()

        # Image upload
        def add_image_to_message():
            if st.session_state.uploaded_img or st.session_state.camera_img:
                img_type = st.session_state.uploaded_img.type if st.session_state.uploaded_img else "image/jpeg"
                raw_img = Image.open(st.session_state.uploaded_img or st.session_state.camera_img)
                img = get_image_base64(raw_img)
                # Appending base64 image URL to the message
                st.session_state.messages.append({
                    "role": "user",
                    "content": [{
                        "type": "image_url",
                        "image_url": {"url": f"data:{img_type};base64,{img}"}
                    }]
                })

        cols_img = st.columns(2)
        with cols_img[0]:
            with st.popover("📁upload"):
                st.file_uploader(
                    "Upload an image",
                    type=["png", "jpg", "jpeg"],
                    accept_multiple_files=False,
                    key="uploaded_img",
                    on_change=add_image_to_message,
                )

        with cols_img[1]:
            with st.popover("📷 Camera"):
                activate_camera = st.checkbox("Activate camera")
                if activate_camera:
                    st.camera_input(
                        "Take a picture",
                        key="camera_img",
                        on_change=add_image_to_message
                    )

        # Audio upload
        st.write("#")
        st.write(" ### **🎤 Add an audio: **")

        audio_prompt = None
        if "prev_speech_hash" not in st.session_state:
            st.session_state.prev_speech_hash = None

        speech_input = audio_recorder("Press to talk:", icon_size="3x", neutral_color="#6ca395")
        if speech_input and st.session_state.prev_speech_hash != hash(speech_input):
            st.session_state.prev_speech_hash = hash(speech_input)
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=("audio.wav", speech_input),
            )
            audio_prompt = transcript.text

        # Chat Input
        if prompt := st.chat_input("Hi! Ask me anything...") or audio_prompt:
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": [{
                        "type": "text",
                        "text": prompt or audio_prompt,
                    }]
                }
            )
            # Displaying the new messages
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                st.write_stream(
                    stream_llm_response(client, model_params)
                )

            # Added audio response (response)
            if audio_response:
                response = client.audio.speech.create(
                    model=tts_model,
                    voice=tts_voice,
                    input=st.session_state.messages[-1]["content"][0]["text"],
                )
                audio_base64 = base64.b64encode(response.content).decode('utf-8')
                audio_html = f""" 
                <audio controls autoplay>
                    <source src="data:audio/wav;base64,{audio_base64}" type="audio/mp3">
                </audio>
                """
            st.html(audio_html)

if __name__ == "__main__":
    main()
