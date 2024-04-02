from utils.singleton import Singleton
from ..repositories.IDatabaseRepository import IDatabaseRepository
from ..entities.Account import Account
from typing import List


class AccountService(metaclass=Singleton):
    databaseRepository: IDatabaseRepository = None

    def __init__(self, databaseRepository: IDatabaseRepository) -> None:
        if self.databaseRepository is None:
            self.databaseRepository = databaseRepository

    def create_account(self, account: Account) -> Account:
        return self.databaseRepository.create_account(account)

    def get_all(self) -> List[Account]:
        return self.databaseRepository.get_all_accounts()
