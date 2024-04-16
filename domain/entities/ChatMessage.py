from pydantic.v1 import BaseModel, Field


class ChatMessage(BaseModel):
    message: str = Field(description="Message")
