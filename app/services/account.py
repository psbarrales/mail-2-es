from infrastructure.database.sql.SQLAlchemyAdapter import SQLAlchemyAdapter
from domain.services.AccountService import AccountService
from domain.entities.Account import Account
from typing import Any, List


class AccountServices:
    accountService: AccountService = None

    def __init__(self) -> None:
        if self.accountService is None:
            self.accountService = AccountService(SQLAlchemyAdapter())

    def create(self, account: Any) -> Account:
        account = Account.parse_obj(account)
        return self.accountService.create_account(account)

    def getAll(self) -> List[Account]:
        return self.accountService.get_all()
