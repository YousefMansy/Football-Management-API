from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from footballfantasyapi.db.base_class import Base


# class PlayerBase(BaseModel):
#     first_name: str
#     last_name: str
#     country: str
#     age: int
#     position: str
#     market_value: int
#

class Player(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(256), nullable=False)
    last_name = Column(String(256), nullable=False)
    country = Column(String(256), nullable=False)
    position = Column(String(256), nullable=False)
    market_value = Column(Integer, nullable=False)
    age = Column(Integer, nullable=False)
    on_transfer_list = Column(Boolean, default=False)
    asking_price = Column(Integer, nullable=True)
    team_id = Column(String(10), ForeignKey("team.id"), nullable=False)
    team = relationship("Team", back_populates="players")
