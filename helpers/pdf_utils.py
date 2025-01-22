
from PyPDF2 import PdfReader

def extract_text_from_pdf(uploaded_file):
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


import streamlit as st
from youtube_transcript_api import (
    YouTubeTranscriptApi, YouTubeRequestFailed, VideoUnavailable, InvalidVideoId, TooManyRequests,
    TranscriptsDisabled, NoTranscriptAvailable, NotTranslatable, TranslationLanguageNotAvailable,
    CookiePathInvalid, CookiesInvalid, FailedToCreateConsentCookie, NoTranscriptFound
)

from pytube import extract



def extract_video_id_from_url(url):
    try:
        return extract.video_id(url)
    except Exception:
        st.error("Please provide a valid YouTube URL.")
        example_urls = [
            'https://www.youtube.com/watch?v=-42K44A1oMA&t=700s',
            'https://www.youtube.com/watch?v=O3BUHwfHf84&t=1812s',
            'https://www.youtube.com/watch?v=Pfy3q6PbbRA',
            'https://www.youtube.com/watch?v=Zq5fmkH0T78',
            'https://www.youtube.com/watch?v=HdWCh_4XE1Q&t=244s',
            'https://www.youtube.com/watch?v=x0uiD362T48'
        ]
        st.info("Here are some valid formats: " + " ,".join(example_urls))
        st.stop()


def get_transcript_text(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([item["text"] for item in transcript])
    except (YouTubeRequestFailed, VideoUnavailable, InvalidVideoId, TooManyRequests, NoTranscriptAvailable, NotTranslatable,
            TranslationLanguageNotAvailable, CookiePathInvalid, CookiesInvalid, FailedToCreateConsentCookie):
        st.error("An error occurred while fetching the transcript. Please try another video.")
        st.stop()    
    except TranscriptsDisabled:
        st.error("Subtitles are disabled for this video. Please try another video.")
        st.stop()
    except NoTranscriptFound:
        st.error("The video doesn't have English subtitles. Please ensure the video you're selecting is in English or has English subtitles available.")
        st.stop()
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}. Please try again.")
        st.stop()
