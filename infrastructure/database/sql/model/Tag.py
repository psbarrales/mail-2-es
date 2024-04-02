from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from ..base import Base


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, autoincrement=True, primary_key=True)
    tag = Column(
        String,
    )
    description = Column(String)
    similarity = Column(ARRAY(String))
