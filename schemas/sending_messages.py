from datetime import datetime
from pydantic import BaseModel, Field

from schemas.bots import BotsView
from schemas.message import MessageView

class SendMessageCreate(BaseModel):
    id_message: int
    sender_bot_id: int
    recipients: list[str]
    sending_time: datetime = Field(default_factory=datetime.now)

class SendingMessageView(BaseModel):
    id: int
    id_message: MessageView
    sender_bot_id: BotsView
    recipients: list[str]
    sending_time: datetime | None

    class Config:
        from_attributes = True
