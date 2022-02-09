import random
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from footballfantasyapi import crud
from footballfantasyapi.api import deps
from footballfantasyapi.schemas import Player, PlayerUpdate, User, PlayerTransfer

router = APIRouter()


@router.get("/player/{player_id}", status_code=200, response_model=Player)
def fetch_player(
        *,
        player_id: int,
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_user)) -> dict:
    """
    Fetch a single player by ID
    """
    result = crud.player.get(db=db, id=player_id)
    if not result:
        raise HTTPException(
            status_code=404, detail=f'Player with ID {player_id} does not exist.'
        )
    return result


@router.post("/player/{player_id}/set_on_transfer_list", status_code=200, response_model=Player)
def set_player_on_transfer_list(
        *,
        player_id: int,
        player_transfer: PlayerTransfer,
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_user)) -> dict:
    """
    Set a player on transfer list.
    """
    player = crud.player.get(db, id=player_id)
    if not player:
        raise HTTPException(
            status_code=400, detail=f"Player with ID: {player_id} not found."
        )
    team = crud.team.get(db, id=player.team_id)
    if team.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail=f"You can only set your own players."
        )

    if player.on_transfer_list:
        raise HTTPException(
            status_code=403, detail=f"Player with ID: {player_id} is already set on transfer list."
        )

    updated_player = crud.player.set_player_on_transfer_list(db=db,
                                                             player_id=player_id,
                                                             player_transfer=player_transfer)
    return updated_player


@router.post("/player/{player_id}/purchase", status_code=200, response_model=Player)
def purchase_player(
        *,
        player_id: int,
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_user)) -> dict:
    """
    Purchase a player that's on the transfer list.
    """
    player = crud.player.get(db, id=player_id)
    if not player:
        raise HTTPException(
            status_code=400, detail=f"Player with ID: {player_id} not found."
        )
    selling_team = crud.team.get(db, id=player.team_id)  # selling team
    if selling_team.user_id == current_user.id:
        raise HTTPException(
            status_code=403, detail=f"You already own this player."
        )

    if not player.on_transfer_list:
        raise HTTPException(
            status_code=403, detail=f"Player with ID: {player_id} is not on transfer list."
        )

    buying_team = crud.team.get_team_by_user_id(db=db, user_id=current_user.id)  # purchasing team
    if player.asking_price > buying_team.funds:
        raise HTTPException(
            status_code=403, detail=f"Insufficient team funds."
        )

    # Update selling team funds and value
    updated_selling_team_funds: int = selling_team.funds + player.asking_price
    crud.team.update_team_funds(db=db, team_id=selling_team.id, funds=updated_selling_team_funds)

    # Update buying team funds and value
    updated_buying_team_funds: int = buying_team.funds - player.asking_price
    crud.team.update_team_funds(db=db, team_id=buying_team.id, funds=updated_buying_team_funds)

    # Calculate new player value
    player_value: int = int(player.market_value * random.uniform(1.1, 2.0))

    # Transfer player
    updated_player = crud.player.transfer_player(db=db, player_id=player_id, team_id=buying_team.id,
                                                 market_value=player_value)

    # Recalculate team values
    crud.team.calculate_team_value(db=db, team_id=buying_team.id)
    crud.team.calculate_team_value(db=db, team_id=selling_team.id)

    return updated_player


@router.put("/{player_id}", status_code=201, response_model=Player)
def update_player(
        *,
        player_id: int,
        player_in: PlayerUpdate,
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_user)) -> dict:
    """
    Update player in the database.
    """
    player = crud.player.get(db, id=player_id)
    if not player:
        raise HTTPException(
            status_code=400, detail=f"Player with ID: {player_id} not found."
        )
    team = crud.team.get(db, id=player.team_id)
    if team.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail=f"You can only update your own players."
        )

    updated_player = crud.player.update(db=db, db_obj=player, obj_in=player_in)

    return updated_player
