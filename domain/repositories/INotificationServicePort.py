from abc import ABC, abstractmethod


class INotificationServicePort(ABC):
    @abstractmethod
    def send_notification(self, message: str):
        pass

    pass
