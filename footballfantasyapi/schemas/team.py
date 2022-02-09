from pydantic import BaseModel, validator
from typing import Sequence, Optional


class TeamBase(BaseModel):
    name: str
    country: str


class TeamCreate(TeamBase):
    name: str
    country: str
    value: int
    funds: int
    user_id: int


class TeamUpdate(TeamBase):
    name: Optional[str]
    country: Optional[str]

    @validator("name")
    def check_name(cls, value):
        if not value:
            raise ValueError("Name cannot be empty.")
        return value

    @validator("country")
    def check_country(cls, value):
        if not value:
            raise ValueError("Country cannot be empty.")
        return value


class TeamInDBBase(TeamBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Team(TeamInDBBase):
    value: int
    funds: int
    pass


# Properties stored in DB
class TeamInDB(TeamInDBBase):
    pass
