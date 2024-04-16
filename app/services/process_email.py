from utils.thread_task import thread_task
from infrastructure.mailing.GmailMailService import GmailMailService
from infrastructure.llm.OpenAILLMFunctions import OpenAILLMFunctions
from infrastructure.database.sql.SQLAlchemyAdapter import SQLAlchemyAdapter
from infrastructure.notification.TelegramNotification import TelegramNotification
from infrastructure.search.ElasticSearchRepository import ElasticSearchRepository
from domain.services.MailService import MailService
from domain.services.TransactionService import TransactionService
from domain.services.NotificationService import NotificationService
from domain.services.RegisterService import RegisterService
from domain.entities.Mail import Mail
from typing import List
import logging

logging.basicConfig(level=logging.INFO)


class ProcessEmailService:
    id: str = None
    mailService: MailService = None
    notificationService: NotificationService = None
    transactionService: TransactionService = None
    registerService: RegisterService = None

    def __init__(self, *args):
        if self.mailService is None:
            self.mailService = MailService(GmailMailService())
        if self.transactionService is None:
            self.transactionService = TransactionService(
                OpenAILLMFunctions(), SQLAlchemyAdapter()
            )
        if self.notificationService is None:
            self.notificationService = NotificationService(
                TelegramNotification(), OpenAILLMFunctions()
            )
        if self.registerService is None:
            self.registerService = RegisterService(
                ElasticSearchRepository(), SQLAlchemyAdapter()
            )

    def run(self):
        mails = self.mailService.get_mails()
        self.process_mails(mails)
        return len(mails)

    @thread_task
    def process_mails(self, mails: List[Mail]):
        for mail in mails:
            try:
                transaction = self.transactionService.get_transaction(mail)
                print("transaction", transaction)
                self.registerService.create_registers(transaction)
                print("register", True)
                # self.notificationService.send_notification(transaction)
                print("notification", True)
                self.mailService.commit(mail.id)
            except Exception as e:
                logging.error(e)
