from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey

from app.footballfantasyapi.db.base_class import Base


class Team(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    country = Column(String(256), nullable=False)
    value = Column(Integer, nullable=False)
    funds = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="teams")
    players = relationship(
        "Player",
        cascade="all,delete-orphan",
        back_populates="team",
        uselist=True)
