from domain.repositories.INotificationServicePort import INotificationServicePort
from domain.repositories.ILLMServicePort import ILLMServicePort
from domain.entities.Transaction import Transaction
from utils.with_retry import with_retry
from datetime import datetime, timedelta
import logging


class NotificationService:
    notificationServicePort: INotificationServicePort
    llmServicePort: ILLMServicePort

    def __init__(
        self,
        notificationServicePort: INotificationServicePort,
        llmServicePort: ILLMServicePort,
    ):
        self.notificationServicePort = notificationServicePort
        self.llmServicePort = llmServicePort

    @with_retry(retries=2, backoff=10)
    def send_notification(self, transaction: Transaction):
        three_days_ago = datetime.now() - timedelta(days=2)
        if transaction.date > three_days_ago and datetime.now() > transaction.date:
            notification = self.llmServicePort.generate_notification(transaction)
            self.notificationServicePort.send_notification(notification.message)
        else:
            logging.info(
                "Notification Omitted: Transaction too old (> 2 days) or is a future.",
            )
