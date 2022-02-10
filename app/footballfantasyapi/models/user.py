from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String

from app.footballfantasyapi.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    teams = relationship(
        "Team",
        cascade="all,delete-orphan",
        back_populates="user",
        uselist=True)
