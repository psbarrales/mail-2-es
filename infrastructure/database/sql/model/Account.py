from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from ..base import Base


class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(
        String,
    )
    primary = Column(Boolean)
    billDate = Column(String)
    billDay = Column(Integer, nullable=True)
    similarity = Column(ARRAY(String))
