from abc import ABC, abstractmethod
from typing import List
from ..entities.Mail import Mail


class IMailingServicePort(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def get_emails(self) -> List[Mail]:
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def commit(self, mail_id):
        pass
