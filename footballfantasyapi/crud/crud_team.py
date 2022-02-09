from typing import Sequence
from sqlalchemy.orm import Session

from footballfantasyapi.models.team import Team
from footballfantasyapi.models.player import Player
from footballfantasyapi.crud.base import CRUDBase
from footballfantasyapi.schemas.team import TeamCreate, TeamUpdate


class CRUDTeam(CRUDBase[Team, TeamCreate, TeamUpdate]):
    ...

    def get_team_by_user_id(self, db: Session, user_id: int) -> Team:
        return db.query(Team).filter(Team.user_id == user_id).first()

    def get_teams_by_user_id(self, db: Session, user_id: int) -> Sequence[Team]:
        return db.query(Team).filter(Team.user_id == user_id).all()


team = CRUDTeam(Team)
