from pydantic.v1 import Field, BaseModel
from typing import List, Optional


class Tag(BaseModel):
    tag: str = Field(description="Tag Name")
    description: Optional[str] = Field(None, description="Tag Description")
    similarity: Optional[List[str]] = Field(None, description="Similarity array list")

    class Config:
        orm_mode = True
