from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from dbase.base_class import Base


class Message(Base):
    id = Column(Integer, primary_key=True)
    subject = Column(String)
    text = Column(String)
    _sending_message_id = relationship("SendingMessages", back_populates="_message_id")
