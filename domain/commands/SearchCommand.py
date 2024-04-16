from pydantic.v1 import BaseModel, Field, validator
from typing import Optional
import json


class SearchCommand(BaseModel):
    host: str = Field(default="0.0.0.0", description="Host for search engine API")
    path: str = Field(
        description="Path for the search engine API after the host",
    )
    method: str = Field(
        description="Method to use on the current API path",
    )
    body: Optional[str] = Field(
        None,
        description="JSON body to send to the API",
    )

    @validator("body", pre=True, allow_reuse=True)
    def check_json(cls, v):
        if v is not None:
            try:
                json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON format")
        return v
