from pydantic.v1 import BaseModel, Field


class Notification(BaseModel):
    language: str = Field(
        default="Spanish",
        description="The language in which the notification will be delivered.",
    )
    personality: str = Field(
        description="Select a personality for the notification to convey."
    )
    style: str = Field(description="Choose a style to add flair to the notification.")
    message: str = Field(
        "Compose a descriptive message to be sent to the user.",
        description="The content of the notification message.",
    )
