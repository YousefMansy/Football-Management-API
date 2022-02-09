from sqlalchemy.orm import Session
from typing import Sequence, Optional, Union

from footballfantasyapi.models.player import Player
from footballfantasyapi.crud.base import CRUDBase
from footballfantasyapi.schemas.player import PlayerCreate, PlayerUpdate, PlayerTransfer, PlayerTransferPrivate


class CRUDPlayer(CRUDBase[Player, PlayerCreate, PlayerUpdate]):
    ...

    def update(
            self,
            db: Session,
            *,
            db_obj: Player,
            obj_in: Union[PlayerUpdate, PlayerTransferPrivate]) -> Player:
        db_obj = super().update(db, db_obj=db_obj, obj_in=obj_in)
        return db_obj

    def set_player_on_transfer_list(self, db: Session, player_id: int, player_transfer: PlayerTransfer) -> Player:
        this_player = self.get(db, id=player_id)
        updated_player: PlayerTransferPrivate = PlayerTransferPrivate(asking_price=player_transfer.asking_price,
                                                                      on_transfer_list=True)
        return self.update(db=db, db_obj=this_player, obj_in=updated_player)

    def get_players_by_team_id(self, db: Session, team_id: int) -> Optional[Sequence[Player]]:
        return db.query(Player).filter(Player.team_id == team_id).all()

    def get_players_on_transfer_list(self, db: Session) -> Optional[Sequence[Player]]:
        return db.query(Player).filter(Player.on_transfer_list).all()

    # def purchase_player(self, db: Session) -> Player:


player = CRUDPlayer(Player)
