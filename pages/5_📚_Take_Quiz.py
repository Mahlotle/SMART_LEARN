# import os
# import streamlit as st
# from helpers.youtube_utils import extract_video_id_from_url, get_transcript_text
# from helpers.openai_utils import get_quiz_data
# from helpers.quiz_utils import string_to_list, get_randomized_options
# from helpers.toast_messages import get_random_toast

# # Set Streamlit page configuration
# st.set_page_config(
#     page_title="QuizTube",
#     page_icon="🧠",
#     layout="centered",
# )

# # Check if user is new or returning using session state
# if 'first_time' not in st.session_state:
#     message, icon = get_random_toast()
#     st.toast(message, icon=icon)
#     st.session_state.first_time = False

# # Title and description
# st.title(":red[Brain Test] — Watch. Learn. Quiz. 🧠", anchor=False)
# st.write("""
# Ever watched a YouTube video and wondered how well you understood its content? Here's a fun twist: 
# Instead of just watching on YouTube, come to **QuizTube** and test your comprehension!

# **How does it work?** 🤔
# 1. Paste the YouTube video URL of your recently watched video.
# 2. Sit back as we craft a custom quiz for you using AI magic! 🪄

# ⚠️ **Important**: The video **must** have English captions for the tool to work.

# Ready? Let’s dive in! 🚀
# """)

# # Retrieve OpenAI API key from environment variable
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# if not OPENAI_API_KEY:
#     st.error("OpenAI API Key is missing! Please set it in your environment variables and restart the app.")
#     st.stop()

# # Form for user input
# with st.form("user_input"):
#     YOUTUBE_URL = st.text_input("Enter the YouTube video link:", 
#                                 value="https://youtu.be/bcYwiwsDfGE?si=qQ0nvkmKkzHJom2y")
#     submitted = st.form_submit_button("Craft my quiz!")

# # Quiz generation and display logic
# if submitted or ('quiz_data_list' in st.session_state):
#     if not YOUTUBE_URL:
#         st.info("Please provide a valid YouTube video link. Head over to [YouTube](https://www.youtube.com/) to fetch one.")
#         st.stop()

#     with st.spinner("Crafting your quiz...🤓"):
#         if submitted:
#             # Process YouTube video and generate quiz
#             video_id = extract_video_id_from_url(YOUTUBE_URL)
#             video_transcription = get_transcript_text(video_id)
#             quiz_data_str = get_quiz_data(video_transcription, OPENAI_API_KEY)
#             st.session_state.quiz_data_list = string_to_list(quiz_data_str)

#             # Initialize session state variables
#             if 'user_answers' not in st.session_state:
#                 st.session_state.user_answers = [None for _ in st.session_state.quiz_data_list]
#             if 'correct_answers' not in st.session_state:
#                 st.session_state.correct_answers = []
#             if 'randomized_options' not in st.session_state:
#                 st.session_state.randomized_options = []

#             # Generate randomized options and correct answers
#             for q in st.session_state.quiz_data_list:
#                 options, correct_answer = get_randomized_options(q[1:])
#                 st.session_state.randomized_options.append(options)
#                 st.session_state.correct_answers.append(correct_answer)

#         # Display the quiz
#         with st.form(key='quiz_form'):
#             st.subheader("🧠 Quiz Time: Test Your Knowledge!", anchor=False)
#             for i, q in enumerate(st.session_state.quiz_data_list):
#                 options = st.session_state.randomized_options[i]
#                 default_index = st.session_state.user_answers[i] if st.session_state.user_answers[i] is not None else 0
#                 response = st.radio(q[0], options, index=default_index)
#                 st.session_state.user_answers[i] = options.index(response)

#             # Submit and evaluate quiz
#             results_submitted = st.form_submit_button(label='Unveil My Score!')

#             if results_submitted:
#                 score = sum([ua == st.session_state.randomized_options[i].index(ca) 
#                              for i, (ua, ca) in enumerate(zip(st.session_state.user_answers, st.session_state.correct_answers))])
#                 st.success(f"Your score: {score}/{len(st.session_state.quiz_data_list)}")

#                 if score == len(st.session_state.quiz_data_list):  # Perfect score
#                     st.balloons()
#                 else:
#                     incorrect_count = len(st.session_state.quiz_data_list) - score
#                     st.warning(f"Almost there! You got {incorrect_count} questions wrong. Let's review them:")

#                 # Show review of answers
#                 for i, (ua, ca, q, ro) in enumerate(zip(st.session_state.user_answers, 
#                                                         st.session_state.correct_answers, 
#                                                         st.session_state.quiz_data_list, 
#                                                         st.session_state.randomized_options)):
#                     with st.expander(f"Question {i + 1}", expanded=False):
#                         if ro[ua] != ca:
#                             st.info(f"Question: {q[0]}")
#                             st.error(f"Your answer: {ro[ua]}")
#                             st.success(f"Correct answer: {ca}")



import os
import streamlit as st
from helpers.pdf_utils import extract_text_from_pdf
from helpers.image_utils import extract_text_from_image
from helpers.openai_utils import get_quiz_data
from helpers.quiz_utils import string_to_list, get_randomized_options
from helpers.toast_messages import get_random_toast

# Set Streamlit page configuration
st.set_page_config(
    page_title="QuizTube",
    page_icon="🧠",
    layout="centered",
)

# Check if user is new or returning using session state
if 'first_time' not in st.session_state:
    message, icon = get_random_toast()
    st.toast(message, icon=icon)
    st.session_state.first_time = False

# Title and description
st.title(":red[Brain Test] — Learn. Test. Quiz. 🧠", anchor=False)
st.write("""
Ever uploaded a document or image and wondered how well you understand it? Now you can test your comprehension by turning your uploaded content into a quiz!

**How does it work?** 🤔
1. Upload your PDF or image.
2. Sit back as we craft a custom quiz for you using AI magic! 🪄

⚠️ **Important**: The uploaded content must contain readable text for the quiz to be generated.

Ready? Let’s dive in! 🚀
""")

# Retrieve OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("OpenAI API Key is missing! Please set it in your environment variables and restart the app.")
    st.stop()

# Form for user input
with st.form("user_input"):
    uploaded_file = st.file_uploader("Upload a PDF or Image", type=["pdf", "png", "jpg", "jpeg"])
    submitted = st.form_submit_button("Craft my quiz!")

# Quiz generation and display logic
if submitted or ('quiz_data_list' in st.session_state):
    if not uploaded_file:
        st.info("Please upload a valid PDF or image file.")
        st.stop()

    with st.spinner("Crafting your quiz...🤓"):
        if submitted:
            # Extract text from the uploaded file
            if uploaded_file.type == "application/pdf":
                document_text = extract_text_from_pdf(uploaded_file)
            else:
                document_text = extract_text_from_image(uploaded_file)

            # Generate quiz data from the extracted text
            quiz_data_str = get_quiz_data(document_text, OPENAI_API_KEY)
            st.session_state.quiz_data_list = string_to_list(quiz_data_str)

            # Initialize session state variables
            if 'user_answers' not in st.session_state:
                st.session_state.user_answers = [None for _ in st.session_state.quiz_data_list]
            if 'correct_answers' not in st.session_state:
                st.session_state.correct_answers = []
            if 'randomized_options' not in st.session_state:
                st.session_state.randomized_options = []

            # Generate randomized options and correct answers
            for q in st.session_state.quiz_data_list:
                options, correct_answer = get_randomized_options(q[1:])
                st.session_state.randomized_options.append(options)
                st.session_state.correct_answers.append(correct_answer)

        # Display the quiz
        with st.form(key='quiz_form'):
            st.subheader("🧠 Quiz Time: Test Your Knowledge!", anchor=False)
            for i, q in enumerate(st.session_state.quiz_data_list):
                options = st.session_state.randomized_options[i]
                default_index = st.session_state.user_answers[i] if st.session_state.user_answers[i] is not None else 0
                response = st.radio(q[0], options, index=default_index)
                st.session_state.user_answers[i] = options.index(response)

            # Submit and evaluate quiz
            results_submitted = st.form_submit_button(label='Unveil My Score!')

            if results_submitted:
                score = sum([ua == st.session_state.randomized_options[i].index(ca) 
                             for i, (ua, ca) in enumerate(zip(st.session_state.user_answers, st.session_state.correct_answers))])
                st.success(f"Your score: {score}/{len(st.session_state.quiz_data_list)}")

                if score == len(st.session_state.quiz_data_list):  # Perfect score
                    st.balloons()
                else:
                    incorrect_count = len(st.session_state.quiz_data_list) - score
                    st.warning(f"Almost there! You got {incorrect_count} questions wrong. Let's review them:")

                # Show review of answers
                for i, (ua, ca, q, ro) in enumerate(zip(st.session_state.user_answers, 
                                                        st.session_state.correct_answers, 
                                                        st.session_state.quiz_data_list, 
                                                        st.session_state.randomized_options)):
                    with st.expander(f"Question {i + 1}", expanded=False):
                        if ro[ua] != ca:
                            st.info(f"Question: {q[0]}")
                            st.error(f"Your answer: {ro[ua]}")
                            st.success(f"Correct answer: {ca}")
