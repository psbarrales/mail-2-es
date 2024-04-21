from domain.entities.ChatMessage import ChatMessage
from domain.entities.Tag import Tag
from domain.entities.Account import Account
from domain.repositories.ILLMAgentPort import ILLMAgentPort
from langchain_community.callbacks import LLMonitorCallbackHandler
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain.globals import set_debug
from langchain.prompts import MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain.tools import StructuredTool
from utils.readfile_content import readfile_content
from dotenv import load_dotenv
from datetime import datetime
from typing import List
import os

load_dotenv()

handler = LLMonitorCallbackHandler()
set_debug(True)

USER_FULL_NAME = os.getenv("USER_FULL_NAME")
USER_DETAILS = os.getenv("USER_DETAILS")
store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


class OpenAILLMAgent(ILLMAgentPort):
    agent: AgentExecutor = None

    def init(self, tools, model_id: str = "gpt-3.5-turbo-1106"):
        llm = None
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    readfile_content("./prompts/agent.md")
                ),
                MessagesPlaceholder(variable_name="chat_history", optional=True),
                HumanMessagePromptTemplate.from_template("{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
        tools_function = [
            StructuredTool.from_function(
                func=tool.method,
                name=tool.name,
                description=tool.description,
            )
            for tool in tools
        ]
        if model_id is not None:
            llm = ChatOpenAI(
                model=model_id,
                temperature=0.5,
                # model="gpt-4-1106-preview",
                callbacks=[handler],
            )
        agent = create_openai_tools_agent(llm, tools_function, prompt)

        self.agent = RunnableWithMessageHistory(
            AgentExecutor(agent=agent, tools=tools_function, verbose=True),
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )

    def run(
        self,
        message: str,
        engine: str,
        index: str,
        schema: str,
        accounts: List[Account],
        tags: List[Tag],
    ) -> ChatMessage:
        now = datetime.now()
        now_datetime = now.strftime("%d/%m/%Y %H:%M:%S")
        accounts_str = (
            "| ID | Name | Bill Date | Primary | Similarity |\n| --- | --- | --- | --- | --- |\n"
            + "\n".join(
                [
                    f"| {account.id} | {account.name} | {account.billDate} | {account.primary} | {', '.join(account.similarity)} |"
                    for account in accounts
                ]
            )
        )
        tags_str = (
            "| Name | Description | Similarity |\n| --- | --- | --- |\n"
            + "\n".join(
                [
                    f"| {tag.tag} | {tag.description} | {', '.join(tag.similarity)} |"
                    for tag in tags
                ]
            )
        )
        response = self.agent.invoke(
            {
                "input": message,
                "datetime": now_datetime,
                "engine": engine,
                "index": index,
                "schema": schema,
                "accounts": accounts_str,
                "tags": tags_str,
            },
            config={"configurable": {"session_id": "default"}},
        )
        return ChatMessage(message=response["output"])
