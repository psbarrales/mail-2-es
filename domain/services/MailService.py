from utils.singleton import Singleton
from ..repositories.IMailingServicePort import IMailingServicePort
from ..entities.Mail import Mail
from typing import List


class MailService(metaclass=Singleton):
    mailingServicePort: IMailingServicePort = None

    def __init__(self, mailingServicePort: IMailingServicePort) -> None:
        if self.mailingServicePort is None:
            self.mailingServicePort = mailingServicePort

    def get_mails(self) -> List[Mail]:
        self.mailingServicePort.connect()
        emails = self.mailingServicePort.get_emails()
        self.mailingServicePort.disconnect()
        return emails

    def commit(self, mail_id):
        self.mailingServicePort.connect()
        self.mailingServicePort.commit(mail_id)
        self.mailingServicePort.disconnect()
