from domain.entities.Account import Account
from domain.entities.Notification import Notification
from domain.entities.Tag import Tag
from domain.entities.Transaction import Transaction
from domain.repositories.ILLMServicePort import ILLMServicePort
from langchain_community.callbacks import LLMonitorCallbackHandler
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain.globals import set_debug
from langchain.output_parsers.openai_functions import PydanticOutputFunctionsParser
from langchain_core.utils.function_calling import (
    convert_to_openai_function,
)
from utils.readfile_content import readfile_content
from utils.with_retry import with_retry
from typing import List
from dotenv import load_dotenv
import random
import string
import os

load_dotenv()

handler = LLMonitorCallbackHandler()
set_debug(True)

USER_FULL_NAME = os.getenv("USER_FULL_NAME")
USER_DETAILS = os.getenv("USER_DETAILS")


class OpenAILLMFunctions(ILLMServicePort):
    llm = ChatOpenAI(
        model="gpt-3.5-turbo-1106",
        temperature=0.5,
        # model="gpt-4-1106-preview",
        callbacks=[handler],
    )
    chain_transaction: LLMChain = None
    chain_notification: LLMChain = None

    def __init__(self) -> None:
        # Transaction
        prompt_transaction = ChatPromptTemplate.from_messages(
            [
                ("system", readfile_content("./prompts/transaction.md")),
                (
                    "user",
                    "Given the following mail: \n```{input}``` extract the transaction",
                ),
            ]
        )
        parser_transaction = PydanticOutputFunctionsParser(pydantic_schema=Transaction)
        openai_functions_transaction = [convert_to_openai_function(Transaction)]
        self.chain_transaction = (
            prompt_transaction
            | self.llm.bind(functions=openai_functions_transaction)
            | parser_transaction
        )

        # Notification
        prompt_notification = ChatPromptTemplate.from_messages(
            [
                ("system", readfile_content("./prompts/notification.md")),
                (
                    "user",
                    "Given the following transaction: \n```{input}``` generate the notification",
                ),
            ]
        )
        parser_notification = PydanticOutputFunctionsParser(
            pydantic_schema=Notification
        )
        openai_functions_notification = [convert_to_openai_function(Notification)]
        self.chain_notification = (
            prompt_notification
            | self.llm.bind(functions=openai_functions_notification)
            | parser_notification
        )

    @with_retry(retries=3, backoff=1)
    def extract_transaction(
        self, mail_content: str, accounts: List[Account], tags: List[Tag]
    ) -> Transaction:
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
        transaction = self.chain_transaction.invoke(
            {
                "input": mail_content,
                "accounts": accounts_str,
                "tags": tags_str,
                "user_full_name": USER_FULL_NAME,
                "user_details": USER_DETAILS,
            }
        )
        return transaction

    @with_retry(retries=2, backoff=1)
    def generate_notification(self, transaction: Transaction) -> Notification:
        sentiment = random.choice(
            [
                "sarcástico",
                "irónico",
                "divertido",
                "gracioso",
                "divertido",
                "extrovertido",
                "introvertido",
                "ambicioso",
                "aventurero",
                "creativo",
                "empático",
                "perfeccionista",
                "sociable",
                "sensible",
                "analítico",
                "espiritual",
                "rebelde",
                "competitivo",
                "humilde",
                "práctico",
            ]
        )
        character = random.choice(
            [
                "si fueras mi contandor",
                "si fueras un personaje medieval",
                "si fueras un personaje de ciencia ficción",
                "si fueras del futuro",
                "si fueras del espacio",
                "si fueras un personaje de fantasía",
                "si fueras un gato",
                "si fueras un perro",
                "robot",
                "Einstein",
                "Batman",
                "Riuk de Death Note",
                "Light de Death Note",
                "L de Death Note",
                "si fueras un Jedi",
                "si fueras un personaje de Harry Potter",
                "si fueras un miembro de los Vengadores",
                "si fueras un personaje de Star Trek",
                "si fueras un personaje de Star Wars",
                "si fueras un personaje de El Señor de los Anillos",
                "si fueras un personaje de Game of Thrones",
                "si fueras un superhéroe",
                "si fueras un supervillano",
                "si fueras un personaje de Disney",
                "si fueras un personaje de Pixar",
                "si fueras un personaje de Marvel",
                "si fueras un personaje de DC Comics",
                "si fueras un personaje de James Bond",
                "si fueras un personaje de Indiana Jones",
                "si fueras un astronauta de la NASA",
                "si fueras un detective privado",
                "si fueras un abogado",
                "si fueras un médico",
                "si fueras un chef",
                "si fueras un deportista profesional",
                "si fueras un músico famoso",
                "si fueras un científico famoso",
                "si fueras un escritor famoso",
                "si fueras un artista famoso",
                "si fueras un personaje de un videojuego famoso",
                "si fueras un personaje de un anime o manga famoso",
                "si fueras un personaje de una serie de televisión famosa",
            ]
        )
        return self.chain_notification.invoke(
            {
                "input": transaction.json(),
                "seed": "".join(random.choices(string.ascii_lowercase, k=20)),
                "sentiment": sentiment,
                "character": character,
            }
        )
