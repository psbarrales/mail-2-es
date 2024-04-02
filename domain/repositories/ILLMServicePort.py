from abc import ABC, abstractmethod
from domain.entities.Account import Account
from domain.entities.Tag import Tag
from domain.entities.Notification import Notification
from domain.entities.Transaction import Transaction
from typing import List


class ILLMServicePort(ABC):
    @abstractmethod
    def extract_transaction(
        self, mail_content: str, accounts: List[Account], tags: List[Tag]
    ) -> Transaction:
        pass

    @abstractmethod
    def generate_notification(self, transaction: Transaction) -> Notification:
        pass
