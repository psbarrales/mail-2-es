from domain.repositories.IDatabaseRepository import IDatabaseRepository
from domain.entities.Account import Account
from domain.entities.Tag import Tag
from typing import List

accounts = []
tags = []


class InMemoryDatabaseRepository(IDatabaseRepository):
    def create_account(self, account: Account) -> Account:
        accounts.append(account)
        return account

    def get_all_accounts(self) -> List[Account]:
        return accounts

    def get_all_tags(self):
        return tags

    def find_account_by_id(self, id: str) -> Account:
        for account in accounts:
            if str(account.id) == id:
                return account
        raise ValueError("Account not found with the given ID")

    def find_tag(self, tag: str) -> Tag:
        for tag in tags:
            if str(tag.tag) == tag:
                return tag
        raise ValueError("Tag not found")
