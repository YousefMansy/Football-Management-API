from typing import Optional
from pydantic import BaseModel, validator


class PlayerBase(BaseModel):
    ...


class PlayerCreate(PlayerBase):
    first_name: str
    last_name: str
    country: str
    age: int
    position: str
    market_value: int
    team_id: int


class PlayerUpdate(PlayerBase):
    first_name: Optional[str]
    last_name: Optional[str]
    country: Optional[str]
    asking_price: Optional[int]

    @validator("first_name")
    def check_first_name(cls, value):
        if not value:
            raise ValueError("First Name cannot be empty.")
        return value

    @validator("last_name")
    def check_last_name(cls, value):
        if not value:
            raise ValueError("Last Name cannot be empty.")
        return value

    @validator("country")
    def check_country(cls, value):
        if not value:
            raise ValueError("Country cannot be empty.")
        return value

    @validator("asking_price")
    def check_asking_price(cls, value):
        if not value:
            raise ValueError("Asking Price cannot be null.")
        return value


class PlayerTransfer(PlayerBase):
    asking_price: int


class PlayerUpdatePrivate(PlayerBase):
    market_value: Optional[int]
    asking_price: Optional[int]
    on_transfer_list: Optional[bool]
    team_id: Optional[int]


class PlayerUpdateRestricted(PlayerBase):
    on_transfer_list: bool


class PlayerInDBBase(PlayerBase):
    id: int
    team_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Player(PlayerInDBBase):
    first_name: str
    last_name: str
    country: str
    age: int
    position: str
    market_value: int
    asking_price: Optional[int]
    on_transfer_list: bool


# Properties stored in DB
class PlayerInDB(PlayerInDBBase):
    pass
