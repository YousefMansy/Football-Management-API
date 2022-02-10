from jose import jwt, JWTError
from pydantic import BaseModel
from typing import Generator, Optional
from sqlalchemy.orm.session import Session
from fastapi import Depends, HTTPException, status

from app.footballfantasyapi.models.user import User
from app.footballfantasyapi.core.config import settings
from app.footballfantasyapi.core.auth import oauth2_scheme
from app.footballfantasyapi.db.session import SessionLocal
from app.footballfantasyapi.clients.base_team_generator import BaseTeamGeneratorClient


class TokenData(BaseModel):
    username: Optional[str] = None


def get_db() -> Generator:
    db = SessionLocal()
    db.current_user_id = None
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user


def get_team_generator_client() -> BaseTeamGeneratorClient:
    return BaseTeamGeneratorClient()
