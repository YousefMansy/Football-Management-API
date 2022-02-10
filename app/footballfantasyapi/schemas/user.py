from typing import Optional, Sequence
from pydantic import BaseModel, EmailStr

from footballfantasyapi.schemas import Team, Player


class UserBase(BaseModel):
    email: Optional[EmailStr] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    email: EmailStr


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties stored in DB but not returned by API
class UserInDB(UserInDBBase):
    hashed_password: str


# Additional properties to return via API
class User(UserInDBBase):
    pass


class Profile(BaseModel):
    user: User
    team: Team
    players: Sequence[Player]
