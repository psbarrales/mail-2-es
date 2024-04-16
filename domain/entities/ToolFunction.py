from pydantic.v1 import BaseModel, Field
from typing import Any, Optional


class ToolFunction(BaseModel):
    name: str = Field(description="Name of the tool")
    description: str = Field(description="Description of the tool")
    args_schema: Optional[Any] = Field(None, description="Arguments for the tools")
    method: Any = Field(description="A callable object")
