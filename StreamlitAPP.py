import os
import json
import pandas as pd
import traceback

from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st
# from langchain.callbacks import get_openai_callback
from langchain_community.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

# Load the response JSON
with open('C:\\Users\\DELL\\Documents\\blockchain\\GenAiProject\\mcq-generator\\Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

# Set page configuration
st.set_page_config(page_title="Advanced MCQ Generator", page_icon="🧠", layout="wide")

# Title and introduction
st.header("🧠 MCQ Generator")
st.write("Generate multiple-choice questions (MCQs) effortlessly from any text. Perfect for educators and content creators.")

# Layout the page into three columns
col1, col2, col3 = st.columns([1, 6, 1])

# Using the middle column for the main content
with col2:
    with st.form("user_inputs"):
        # File uploader in a wide format
        uploaded_files = st.file_uploader("📁 Upload a PDF or txt file", accept_multiple_files=False)

        # Sliders for MCQ count
        mcq_count = st.slider("Number of MCQs", min_value=3, max_value=50, value=10)

        # Subject input with a placeholder
        subject = st.text_input("📚 Subject", placeholder="Enter the subject here")

        # Complexity level selection
        tone = st.selectbox("Complexity Level of Questions", ["Simple", "Medium", "Complex"], index=0)

        # Submit button for the form
        submit_button = st.form_submit_button("Generate MCQs 🚀")

        if submit_button and uploaded_files is not None and subject and tone:
            with st.spinner("✨ Generating MCQs... Please wait."):
                try:
                    # Read the uploaded file
                    text = read_file(uploaded_files)

                    # Use the openai callback for processing
                    with get_openai_callback() as cb:
                        response = generate_evaluate_chain(
                            {
                                "text": text,
                                "number": mcq_count,
                                "subject": subject,
                                "tone": tone,
                                "response_json": json.dumps(RESPONSE_JSON)
                            }
                        )

                except Exception as e:
                    traceback.print_exception(type(e), e, e.__traceback__)
                    st.error(f"❌ Error: {e}")

                else:
                    # Display the token and cost information
                    st.sidebar.write(f"Total Tokens: {cb.total_tokens}")
                    st.sidebar.write(f"Prompt Tokens: {cb.prompt_tokens}")
                    st.sidebar.write(f"Completion Tokens: {cb.completion_tokens}")
                    st.sidebar.write(f"Total Cost: {cb.total_cost}")

                    if isinstance(response, dict):
                        quiz = response.get('quiz', None)
                        if quiz is not None:
                            table_data = get_table_data(quiz)
                            if table_data is not None:
                                df = pd.DataFrame(table_data)
                                df.index += 1
                                st.success("✅ MCQs Generated Successfully!")
                                st.table(df)

                                # Review section with pre-populated text
                                st.text_area("📝 Review", value=response.get("review", ""))
                            else:
                                st.error("❌ Error in the table data")
                    else:
                        st.write(response)
