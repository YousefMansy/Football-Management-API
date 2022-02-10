from sqlalchemy.orm import Session
from typing import Sequence, Optional, Union

from footballfantasyapi.models.player import Player
from footballfantasyapi.crud.base import CRUDBase
from footballfantasyapi.schemas.player import PlayerCreate, PlayerUpdate, PlayerTransfer, PlayerUpdatePrivate


class CRUDPlayer(CRUDBase[Player, PlayerCreate, PlayerUpdate]):
    ...

    def update(
            self,
            db: Session,
            *,
            db_obj: Player,
            obj_in: Union[PlayerUpdate, PlayerUpdatePrivate]) -> Player:
        db_obj = super().update(db=db, db_obj=db_obj, obj_in=obj_in)
        return db_obj

    def set_player_on_transfer_list(self, db: Session, player_id: int, player_transfer: PlayerTransfer) -> Player:
        this_player = self.get(db=db, id=player_id)
        updated_player: PlayerUpdatePrivate = PlayerUpdatePrivate(asking_price=player_transfer.asking_price,
                                                                  on_transfer_list=True)
        return self.update(db=db, db_obj=this_player, obj_in=updated_player)

    def get_players_by_team_id(self, db: Session, team_id: int) -> Optional[Sequence[Player]]:
        return db.query(Player).filter(Player.team_id == team_id).all()

    def get_players_on_transfer_list(self, db: Session) -> Optional[Sequence[Player]]:
        return db.query(Player).filter(Player.on_transfer_list).all()

    def transfer_player(self, db: Session, player_id: int, team_id: int, market_value: int) -> Player:
        this_player = self.get(db=db, id=player_id)
        updated_player: PlayerUpdatePrivate = PlayerUpdatePrivate(market_value=market_value,
                                                                  on_transfer_list=False,
                                                                  team_id=team_id)
        return self.update(db=db, db_obj=this_player, obj_in=updated_player)


player = CRUDPlayer(Player)
