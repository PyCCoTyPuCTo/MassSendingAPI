from pydantic import BaseModel


class MessageCreate(BaseModel):
    subject: str
    text: str

class MessageView(BaseModel):
    id: int
    subject: str
    text: str

    class Config:
        from_attributes = True
