from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EmailCreate(BaseModel):
    sender: str = Field(min_length=3, max_length=255)
    subject: str = Field(min_length=1, max_length=255)
    body: str = Field(min_length=1, max_length=20000)


class EmailRead(EmailCreate):
    id: int
    received_at: datetime

    model_config = ConfigDict(from_attributes=True)