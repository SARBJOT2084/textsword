from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import google.generativeai as genai
import os 
import streamlit as st
from dotenv import load_dotenv
import pyperclip
app = FastAPI()

load_dotenv()

API_KEY=os.getenv('API_KEY')
# Define your Gemini API key and model

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')


# Function to copy text to the clipboard
def copy_to_clipboard(text):
    pyperclip.copy(text)
    st.success("Text copied to clipboard!")
    st.session_state.show_popup = True

    # Check if the pop-up should be shown
    if st.session_state.get('show_popup', False):
        st.write("<div style='background-color: #f0f0f5; padding: 20px; border-radius: 5px;'>This is the message in the pop-up</div>", unsafe_allow_html=True)
        if st.button("Close"):
            st.session_state.show_popup = False

# Function to display a card with optional actions
def display_card_with_actions(content, title):
    if content:
        st.title(title)
        st.text_area(label="Result", value=content, height=800, key="text_area", disabled=True)


def call_gemini(option,prompt):
    new_prompt=prompt
    if option=="summary":
        new_prompt=f"""
            Summarize the below given text into points not exceeding more than 70 words:
            {prompt}
        """
    elif option=="grammer":
        new_prompt=f"""
        Please correct the grammer for below prompt.
        {prompt}
    """
        #information
    else:
        new_prompt=f"""
            Provide relevant and recent information about the below topic in brief:
            {prompt}
    """
    
    response = model.generate_content(new_prompt)
        
    return response.text

# Streamlit UI

custom_font = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Style+Script&display=swap');

.custom-font {
    font-family: "Style", cursive;
    font-weight:600;
    font-size: 50px;
    color: #4A90E2;
}

.custom-font > p {
    font-size: 50px;
}
</style>
<div class="custom-font">
    <p>TextSword&#x2694;</p>
</div>
"""

# Use st.write to render the custom HTML
st.write(custom_font, unsafe_allow_html=True)

st.write("Words are mightier than the sword ....")
st.sidebar.title("Features")
feature = st.sidebar.selectbox(
    "Choose a feature:",
    ["Summarize Your Points", "Correct Grammar", "Info About Any Topic"]
)

if feature == "Summarize Your Points":
    st.header("Summarize Your Points")
    text_to_summarize = st.text_area("Enter text to summarize")
    if st.button("Summarize"):
        if text_to_summarize:
            summary = call_gemini("summary",text_to_summarize)
            if summary:
                display_card_with_actions(summary, "Summary")
        else:
            st.warning("Please enter some text to summarize.")

elif feature == "Correct Grammar":
    st.header("Correct Grammar")
    text_to_improve = st.text_area("Enter text to correct grammar")
    if st.button("Improve"):
        if text_to_improve:
            improved_text = call_gemini("grammer",text_to_improve)
            if improved_text:
                display_card_with_actions(improved_text, "Improved Text")
        else:
            st.warning("Please enter text to correct grammar.")

elif feature == "Info About Any Topic":
    st.header("Info About Any Topic")
    topic_to_search = st.text_input("Enter topic to get information")
    if st.button("Get Information"):
        if topic_to_search:
            information = call_gemini("information",topic_to_search)
            if information:
                display_card_with_actions(information,"Brief Information")
        else:
            st.warning("Please enter a topic to search.")
