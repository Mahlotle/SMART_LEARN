import streamlit as st

# Function to set the CSS for the chosen theme
def set_theme(theme):
    if theme == 'Light':
        st.markdown("""
            <style>
                body {
                    background-color: #ffffff;
                    color: #333;
                }
                h1, h2, h3, h4, h5, h6 {
                    color: #4CAF50;
                }
                .stButton>button {
                    background-color: #8BC34A;
                    color: white;
                }
            </style>
        """, unsafe_allow_html=True)
    elif theme == 'Dark':
        st.markdown("""
            <style>
                body {
                    background-color: #333;
                    color: #fff;
                }
                h1, h2, h3, h4, h5, h6 {
                    color: #FF5722;
                }
                .stButton>button {
                    background-color: #FF9800;
                    color: white;
                }
            </style>
        """, unsafe_allow_html=True)
    elif theme == 'Blue':
        st.markdown("""
            <style>
                body {
                    background-color: #e3f2fd;
                    color: #0d47a1;
                }
                h1, h2, h3, h4, h5, h6 {
                    color: #0288d1;
                }
                .stButton>button {
                    background-color: #0288d1;
                    color: white;
                }
            </style>
        """, unsafe_allow_html=True)

# Set the page title and layout
st.set_page_config(page_title="AI Tutor App", page_icon="📚", layout="centered")

# Title of the app
st.title("Welcome to the AI Tutor App 🎓")

# Theme selection dropdown
theme = st.selectbox('Choose your theme:', ['Light', 'Dark', 'Blue'])

# Apply selected theme
set_theme(theme)

# App description with added emojis and color
st.markdown("""
    <div style="font-size: 18px;">
        This AI-powered tutoring app helps you learn and improve in a wide variety of subjects. 
        Whether you need help with <strong style="color: #FF5722;">math</strong>, <strong style="color: #2196F3;">science</strong>, 
        <strong style="color: #9C27B0;">language</strong>, or any other field, our intelligent tutor is here to guide you through. 
        The AI tutor provides personalized learning experiences, step-by-step explanations, and interactive exercises to enhance your learning.
    </div>
""", unsafe_allow_html=True)

# Add a feature description with colorful bullets
st.subheader("🔑 Key Features of the AI Tutor App:")

st.markdown("""
    <ul style="font-size: 16px;">
        <li><strong style="color: #8BC34A;">Personalized Lessons</strong>: Tailored learning paths based on your progress and goals. 📚</li>
        <li><strong style="color: #03A9F4;">Interactive Exercises</strong>: Engage with quizzes and challenges to reinforce what you've learned. 🧩</li>
        <li><strong style="color: #FF9800;">24/7 Availability</strong>: Get help whenever you need it. ⏰</li>
        <li><strong style="color: #9C27B0;">Step-by-step Explanations</strong>: Complex topics are broken down for easier understanding. ✨</li>
    </ul>
""", unsafe_allow_html=True)

# Call to action to get started with a playful emoji
st.subheader("🚀 Ready to start ?")
st.write("Choose any option on the sidebar to get an  AI assistance of your preference: 📖")

# Footer with footer emoji and custom color
st.markdown("""
    ---
    <div style="text-align: center; font-size: 14px;">
        Powered by <strong>AI Tutor App</strong> | All rights reserved 🛠️
    </div>
""", unsafe_allow_html=True)
