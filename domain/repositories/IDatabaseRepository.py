from abc import ABC, abstractmethod
from typing import List
from ..entities.Account import Account
from ..entities.Tag import Tag


class IDatabaseRepository(ABC):
    @abstractmethod
    def create_account(self, account: Account) -> Account:
        pass

    @abstractmethod
    def get_all_accounts(self) -> List[Account]:
        pass

    @abstractmethod
    def find_account_by_id(self, id: str) -> Account:
        pass

    @abstractmethod
    def create_tag(self, tag: Tag) -> Tag:
        pass

    @abstractmethod
    def get_all_tags(self) -> List[Tag]:
        pass

    @abstractmethod
    def find_tag(self, tag: str) -> Tag:
        pass
