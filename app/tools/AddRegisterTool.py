from utils.thread_task import thread_task
from infrastructure.mailing.GmailMailService import GmailMailService
from infrastructure.llm.OpenAILLMFunctions import OpenAILLMFunctions
from infrastructure.database.sql.SQLAlchemyAdapter import SQLAlchemyAdapter
from infrastructure.notification.TelegramBot import TelegramBot
from infrastructure.search.ElasticSearchRepository import ElasticSearchRepository
from domain.services.MailService import MailService
from domain.services.NotificationService import NotificationService
from domain.services.RegisterService import RegisterService
from domain.entities.Mail import Mail
from typing import List
import logging
from datetime import datetime


class AddRegisterTool:
    registerService: RegisterService = None

    def __init__(self):
        if self.registerService is None:
            self.registerService = RegisterService(
                OpenAILLMFunctions(), ElasticSearchRepository(), SQLAlchemyAdapter()
            )

    def run(self, message_content: str):
        now = datetime.now()
        transaction = self.registerService.get_transaction(
            Mail(
                subject="New message transaction",
                content=message_content,
                date=now.strftime("%d/%m/%Y %H:%M:%S"),
            )
        )
        print("transaction", transaction)
        self.registerService.create_registers(transaction)
        print("register", True)
        return f"Transaction process successfully: {transaction.json()}"
