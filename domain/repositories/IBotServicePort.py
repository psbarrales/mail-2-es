from abc import ABC, abstractmethod
from typing import Any


class IBotServicePort(ABC):
    @abstractmethod
    def init(self, func: Any):
        pass

    pass
