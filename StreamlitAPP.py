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


with open('C:\\Users\\DELL\\Documents\\blockchain\\GenAiProject\\mcq-generator\\Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)


st.set_page_config(page_title="Advanced MCQ Generator", page_icon="🧠", layout="wide")


st.markdown("<h1 style='text-align: center;'>🧠 MCQ Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Generate multiple-choice questions (MCQs) effortlessly from any text or pdf. Perfect for educators and content creators.</p>", unsafe_allow_html=True)


col1, col2, col3 = st.columns([1, 6, 1])


with col2:
    with st.form("user_inputs"):
        
        uploaded_files = st.file_uploader("📁 Upload a PDF or txt file", accept_multiple_files=False)

        
        mcq_count = st.slider("Number of MCQs", min_value=1, max_value=50, value=10)

    
        subject = st.text_input("📚 Subject", placeholder="Enter the subject here")

        
        tone = st.selectbox("Complexity Level of Questions", ["Simple", "Medium", "Complex"], index=0)

        
        submit_button = st.form_submit_button("Generate MCQs 🚀")

        if submit_button and uploaded_files is not None and subject and tone:
            with st.spinner("✨ Generating MCQs... Please wait."):
                try:
                    
                    text = read_file(uploaded_files)

                    
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
                    
                    print(f"Total Tokens: {cb.total_tokens}")
                    print(f"Prompt Tokens: {cb.prompt_tokens}")
                    print(f"Completion Tokens: {cb.completion_tokens}")
                    print(f"Total Cost: {cb.total_cost}")

                    if isinstance(response, dict):
                        quiz = response.get('quiz', None)
                        if quiz is not None:
                            table_data = get_table_data(quiz)
                            if table_data is not None:
                                df = pd.DataFrame(table_data)
                                df.index += 1
                                st.success("✅ MCQs Generated Successfully!")
                                st.table(df)

                                
                                st.text_area(label="📝 Review", value=response["review"])
                            else:
                                st.error("❌ Error in the table data")
                    else:
                        st.write(response)
