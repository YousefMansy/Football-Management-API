from sqlalchemy.orm import Session
from typing import Any, Dict, Optional, Union

from app.footballfantasyapi.crud import team, player
from app.footballfantasyapi.models.user import User
from app.footballfantasyapi.crud.base import CRUDBase
from app.footballfantasyapi.core.security import get_password_hash
from app.footballfantasyapi.schemas.user import UserCreate, UserUpdate, Profile


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        create_data = obj_in.dict()
        create_data.pop("password")
        db_obj = User(**create_data)
        db_obj.hashed_password = get_password_hash(obj_in.password)
        db.add(db_obj)
        db.commit()

        return db_obj

    def update(self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_profile(self, db: Session, user_id: int) -> Profile:
        this_user = self.get(db=db, id=user_id)
        this_team = team.get_team_by_user_id(db=db, user_id=this_user.id)
        team_players = player.get_players_by_team_id(db=db, team_id=this_team.id)
        return Profile(user=this_user, team=this_team, players=team_players)


user = CRUDUser(User)
