from pydantic.v1 import BaseModel, Field


class Mail(BaseModel):
    id: str = Field(None)
    subject: str = Field(description="Subject of the email.")
    content: str = Field(description="Content of the email.")
    date: str = Field(description="Date of the email.")

    def to_str(self):
        return f"Date: {self.date}\nSubject: {self.subject}\nBody: {self.content}"
