from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from dbase.base_class import Base


class SocialNetworks(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    _social_network_bot = relationship("Bots", back_populates="_social_networks")
