import names
import random
from sqlalchemy.orm import Session
from typing import Tuple, Sequence
from fastapi import APIRouter, Depends, HTTPException

from footballfantasyapi import crud
from footballfantasyapi.api import deps
from footballfantasyapi.core.config import settings
from footballfantasyapi.schemas import User, UserCreate, Player, PlayerCreate, Team, TeamCreate, Profile

router = APIRouter()


def generate_players(db: Session, team_id: int) -> Sequence[Player]:
    team_players = []
    for pos, value in settings.INITIAL_TEAM_STRUCTURE.items():
        for i in range(value):
            player_in = PlayerCreate(
                first_name=names.get_first_name(),
                last_name=names.get_last_name(),
                country='Egypt',
                age=random.randint(18, 40),
                position=pos,
                market_value=settings.INITIAL_PLAYER_VALUE,
                team_id=team_id
            )
            player: Player = crud.player.create(db=db, obj_in=player_in)
            team_players.append(player)
    return team_players


def generate_team(db: Session, user_id: int) -> Team:
    team_in = TeamCreate(
        name='Liverpool',
        country='United Kingdom',
        value=settings.INITIAL_PLAYER_VALUE * settings.INITIAL_PLAYERS_COUNT,
        funds=settings.INITIAL_TEAM_FUNDS,
        user_id=user_id
    )
    team: Team = crud.team.create(db=db, obj_in=team_in)

    return team


@router.post("/user", status_code=201, response_model=Profile)
def create_user(
        *,
        user_in: UserCreate,
        db: Session = Depends(deps.get_db)) -> dict:
    """
    Create a new User
    """
    user = crud.user.create(db=db, obj_in=user_in)
    team = generate_team(db=db, user_id=user.id)
    team_players = generate_players(db=db, team_id=team.id)
    return {'user': user, 'team': team, 'players': team_players}


@router.get("/user/{user_id}", status_code=200, response_model=User)
def fetch_user(
        *,
        user_id: int,
        db: Session = Depends(deps.get_db)) -> dict:
    """
    Fetch a single user by ID
    """

    result = crud.user.get(db=db, id=user_id)
    if not result:
        raise HTTPException(
            status_code=404, detail=f'User with ID {user_id} does not exist.'
        )
    return result
