from abc import ABC, abstractmethod
from ..entities.Register import Register
from typing import List


class ISearchRepository(ABC):
    @abstractmethod
    def store_register(self, register: List[Register]):
        pass
