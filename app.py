from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
from typing import Any

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from tools import calculator, word_counter

# Load API key from .env
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

##Gemini Model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0
)

#tool
tools = [calculator, word_counter]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. "
            "You can answer questions using your own knowledge. "
            "Use tools only when necessary. "
            "If a question requires calculation, use the calculator tool. "
            "If a question asks for word count, use the word_counter tool.",
        ),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ]
)

# create agent
agent = create_tool_calling_agent(
    llm,
    tools,
    prompt
)

# agent executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

def my_output(query) -> Any:
    result = agent_executor.invoke({"input": query})
    return result["output"]

#ui
st.set_page_config(page_title="AI Agent")
st.title("AI Agent with Gemini Model")
query = st.text_input("Enter your query:")
if st.button("Submit"):
    response = my_output(query)
    st.subheader("Response:")
    st.write(response)
