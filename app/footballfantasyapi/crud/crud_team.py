from typing import Sequence, Union
from sqlalchemy.orm import Session

from app.footballfantasyapi.crud import player
from app.footballfantasyapi.models.team import Team
from app.footballfantasyapi.crud.base import CRUDBase
from app.footballfantasyapi.schemas.player import Player
from app.footballfantasyapi.schemas.team import TeamCreate, TeamUpdate, TeamUpdatePrivate


class CRUDTeam(CRUDBase[Team, TeamCreate, TeamUpdate]):
    ...

    def update(
            self,
            db: Session,
            *,
            db_obj: Team,
            obj_in: Union[TeamUpdate, TeamUpdatePrivate]) -> Team:
        db_obj = super().update(db=db, db_obj=db_obj, obj_in=obj_in)
        return db_obj

    def get_team_by_user_id(self, db: Session, user_id: int) -> Team:
        return db.query(Team).filter(Team.user_id == user_id).first()

    def get_teams_by_user_id(self, db: Session, user_id: int) -> Sequence[Team]:
        return db.query(Team).filter(Team.user_id == user_id).all()

    def update_team_funds(self, db: Session, team_id: int, funds: int) -> Team:
        this_team: Team = self.get(db=db, id=team_id)
        updated_team: TeamUpdatePrivate = TeamUpdatePrivate(funds=funds)
        return self.update(db=db, db_obj=this_team, obj_in=updated_team)

    def calculate_team_value(self, db: Session, team_id: int) -> Team:
        players: Sequence[Player] = player.get_players_by_team_id(db=db, team_id=team_id)
        value: int = sum([p.market_value for p in players]) if players else 0
        this_team: Team = self.get(db=db, id=team_id)
        updated_team: TeamUpdatePrivate = TeamUpdatePrivate(value=value)
        return self.update(db=db, db_obj=this_team, obj_in=updated_team)


team = CRUDTeam(Team)
