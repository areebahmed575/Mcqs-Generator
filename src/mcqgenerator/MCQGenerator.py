import os
import json
import pandas as pd
import traceback


from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.callbacks import get_openai_callback
import PyPDF2
from dotenv import load_dotenv



load_dotenv()  # take environment variables from .env.

KEY=os.getenv("OPENAI_API_KEY")