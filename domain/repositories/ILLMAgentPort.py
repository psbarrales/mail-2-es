from abc import ABC, abstractmethod
from domain.entities.Account import Account
from domain.entities.ChatMessage import ChatMessage
from domain.entities.Tag import Tag
from domain.entities.ToolFunction import ToolFunction
from typing import List


class ILLMAgentPort(ABC):
    @abstractmethod
    def init(self, tools: List[ToolFunction]) -> None:
        pass

    @abstractmethod
    def run(
        self,
        message: str,
        engine: str,
        index: str,
        schema: str,
        accounts: List[Account],
        tags: List[Tag],
    ) -> ChatMessage:
        pass
