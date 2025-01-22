import streamlit as st
from openai import OpenAI
import pdfplumber
from dotenv import load_dotenv
import os

load_dotenv()

# Access the API key from the environment
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("OpenAI API key is missing. Please add it to the .env file.")

client = OpenAI(api_key=openai_api_key)

# Reads and returns the text context of a PDF using pdfplumber
def read_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:  
        for page in pdf.pages:
            text += page.extract_text()
    return text

def ask_question(document_text, question, withStreaming=True):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"""Document: {document_text}\nQuestion: {question}, Return the answer in the form of Markdown for formatting"""}
        ],
        n=1,
        stop=None,
        max_tokens=250,
        temperature=0.7,
        stream=withStreaming,
    )
    
    if withStreaming:
        collected_messages = []  # Make sure this is initialized properly
        placeholder = st.empty()  # Display placeholder for streaming
        
        # Initialize display handle for formatted output
        for chunk in response:
            collected_message = chunk.choices[0].delta.content
            if collected_message is not None:  # Only append if it's not None
                collected_messages.append(collected_message)  # Append to list directly
            current_text = ''.join(collected_messages)  # Join all collected parts together
            placeholder.markdown(current_text)  # Display the collected messages in real-time
        
        answer = ''.join(collected_messages)  # After stream ends, collect full answer
    else:
        answer = response.choices[0].message.content
        st.markdown(answer)
    
    return answer
st.set_page_config(page_title="Chat Docs", page_icon="📖", layout="centered")
st.title("Chat with your document📖")
st.write("Upload a PDF document and ask a question about its content")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file is not None:
    document_text = read_pdf(uploaded_file)
    st.success("PDF document uploaded and processed successfully")

    question = st.text_input("Enter your question")
    if st.button("Get the answer"):
        with st.spinner("Getting the answer..."):
            answer = ask_question(document_text, question)
        st.success("Answer retrieved successfully")
else:
    st.warning("Please upload a PDF document.🗎 ")