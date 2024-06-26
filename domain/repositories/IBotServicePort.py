from abc import ABC, abstractmethod
from typing import Any


class IBotServicePort(ABC):
    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def on_message(self, func: Any):
        pass

    @abstractmethod
    def on_command(self, command_name: str, func: Any):
        pass
