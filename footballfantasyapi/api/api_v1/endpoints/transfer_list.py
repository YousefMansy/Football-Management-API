from typing import Sequence
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from footballfantasyapi import crud
from footballfantasyapi.api import deps
from footballfantasyapi.schemas import Team, Player

router = APIRouter()


@router.get("/show", status_code=200, response_model=Sequence[Player])
def get_transfer_list(
        *,
        db: Session = Depends(deps.get_db)) -> Sequence[Player]:
    """
    Show all players available for transfer
    """
    result = crud.player.get_players_on_transfer_list(db=db)
    return result
