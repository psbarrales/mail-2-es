from utils.singleton import Singleton
from ..repositories.IDatabaseRepository import IDatabaseRepository
from ..entities.Tag import Tag
from typing import List


class TagService(metaclass=Singleton):
    databaseRepository: IDatabaseRepository = None

    def __init__(self, databaseRepository: IDatabaseRepository) -> None:
        if self.databaseRepository is None:
            self.databaseRepository = databaseRepository

    def create_tag(self, account: Tag) -> Tag:
        return self.databaseRepository.create_tag(account)

    def get_all(self) -> List[Tag]:
        return self.databaseRepository.get_all_tags()
