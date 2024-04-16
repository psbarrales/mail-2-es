from abc import ABC, abstractmethod
from ..entities.Register import Register
from ..commands.SearchCommand import SearchCommand
from typing import List


class ISearchRepository(ABC):
    engine = "Default Search Engine"
    index = "registers"
    command_schema = SearchCommand

    @abstractmethod
    def store_register(self, register: List[Register]):
        pass

    @abstractmethod
    def search_command(self, command: SearchCommand):
        pass
