from sqlalchemy import ARRAY, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from dbase.base_class import Base


class SendingMessages(Base):
    id = Column(Integer, primary_key=True, index=True)
    id_message = Column(Integer, ForeignKey("message.id"))
    sender_bot_id = Column(Integer, ForeignKey("bots.id"))
    recipients = Column(ARRAY(String))
    sending_time = Column(DateTime(timezone=True))
    _message_id = relationship("Message", back_populates="_sending_message_id")
    _sender_bot_id = relationship("Bots", back_populates="_sending_message_id")
