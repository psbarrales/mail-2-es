from langchain_community.callbacks import LLMonitorCallbackHandler
from langchain_openai import ChatOpenAI
# from langchain_groq import ChatGroq
# import os

handler = LLMonitorCallbackHandler()

llm: ChatOpenAI = ChatOpenAI(
    model="gpt-3.5-turbo-1106",
    temperature=0.5,
    callbacks=[handler],
)

# llm: ChatOpenAI = ChatOpenAI(
#     base_url="https://api.together.xyz/v1",
#     api_key=os.environ["TOGETHER_API_KEY"],
#     model="mistralai/Mixtral-8x22B-Instruct-v0.1",
#     temperature=0.5,
#     streaming=False,
#     callbacks=[handler],
# )

# llm: ChatGroq = ChatGroq(temperature=0.5, model_name="mixtral-8x7b-32768")
