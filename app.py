import google.generativeai as genai
import os 
import streamlit as st
from dotenv import load_dotenv
import pyperclip

load_dotenv()

API_KEY=os.getenv('API_KEY')
# Define your Gemini API key and model

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to copy text to the clipboard

cont=""
custom_style = f"""

        <style>
            .custom-text-area {{
                width: 100%;
                height: 500px;
                border: 1px solid #ddd;
                padding: 10px;
                background-color: #f9f9f9;
                color: black;
                font-family: sans-serif;
                font-size: 14px;
                overflow-y: auto;
                box-sizing: border-box;
            }}
            .custom-text-area:disabled {{
                background-color: #f9f9f9;
                cursor: not-allowed;
            }}
        </style>
        <textarea class="custom-text-area" disabled>{cont}</textarea>
"""

# Function to display a card with optional actions
def display_card_with_actions(content, title):
    if content:
        st.title(title)
        st.write(content)
        if st.button("Copy text"):
            pyperclip.copy(content)
            st.write("Successfully copied")
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
    ["Summarize Your Notes", "Correct Grammar", "Info About Any Topic"]
)

if feature == "Summarize Your Notes":
    st.header("Summarize Your Notes")
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
