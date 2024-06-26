from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from dbase.base_class import Base

class Bots(Base):
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, nullable=False)
    password = Column(String)
    owner_id = Column(Integer, ForeignKey("user.id"))
    social_network_id = Column(Integer, ForeignKey("socialnetworks.id"))
    is_active = Column(Boolean, default=True)
    _bot_owner = relationship("User", back_populates="_owners_bots")
    _social_networks = relationship("SocialNetworks", back_populates="_social_network_bot")
    _sending_message_id = relationship("SendingMessages", back_populates="_sender_bot_id")