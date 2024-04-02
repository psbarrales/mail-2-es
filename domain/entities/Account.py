from pydantic.v1 import BaseModel, Field
from typing import List, Optional


class Account(BaseModel):
    id: Optional[int] = Field(None, description="Incremental ID")
    name: str = Field(description="Account Name")
    primary: bool = Field(True)
    billDate: Optional[str] = Field("Same transaction date", description="Billing Date")
    billDay: Optional[int] = Field(0, description="Billing Day")
    similarity: Optional[List[str]] = Field([], description="Similarity array list")

    class Config:
        orm_mode = True
