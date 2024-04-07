import os
import json
import pandas as pd
import traceback

from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
import streamlit as st
#from langchain.callbacks import get_openai_callback
from langchain_community.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging


with open("C:\Users\DELL\Documents\blockchain\GenAiProject\mcq-generator\Response.json", 'r') as file:
    RESPONSE_JSON = json.load("file")