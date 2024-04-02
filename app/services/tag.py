from utils.singleton import Singleton
from infrastructure.database.sql.SQLAlchemyAdapter import SQLAlchemyAdapter
from domain.services.TagService import TagService
from domain.entities.Tag import Tag
from typing import Any, List


class TagServices:
    tagService: TagService = None

    def __init__(self) -> None:
        if self.tagService is None:
            self.tagService = TagService(SQLAlchemyAdapter())

    def create(self, account: Any) -> Tag:
        account = Tag.parse_obj(account)
        return self.tagService.create_tag(account)

    def getAll(self) -> List[Tag]:
        return self.tagService.get_all()
