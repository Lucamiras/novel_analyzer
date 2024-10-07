import os
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st


os.environ["GOOGLE_API_KEY"] = st.secrets["GEMINI_FLASH_SECRET"]
prompt = [
    (
        "system",
        """You are a seasoned literary agent. You have been tasked with helping writers hone their craft. You have been given a manuscript to review. 
        Write a short analysis and present it as if you were giving feedback to the author in person. Do not respond in bullet points. 
        Present your response as if you're in dialogue with the author:"""
    ),
    ("human", "{text}")
]

class LiteraryCritic:
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.8,
        max_tokens=None,
        timeout=None,
        max_retries=2
    )
