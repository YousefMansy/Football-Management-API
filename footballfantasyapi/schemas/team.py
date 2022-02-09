from typing import Optional
from pydantic import BaseModel, validator


class TeamBase(BaseModel):
    ...


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


class TeamUpdatePrivate(TeamBase):
    funds: Optional[int]
    value: Optional[int]


class TeamInDBBase(TeamBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Team(TeamInDBBase):
    id: int
    name: str
    country: str
    value: int
    funds: int
    user_id: int
    pass


# Properties stored in DB
class TeamInDB(TeamInDBBase):
    pass
