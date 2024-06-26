from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from dbase.base_class import Base


class User(Base):
    id =Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    _owners_bots = relationship("Bots", back_populates="_bot_owner")