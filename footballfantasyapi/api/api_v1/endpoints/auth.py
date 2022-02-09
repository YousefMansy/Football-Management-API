from typing import Any, Sequence, List
from sqlalchemy.orm.session import Session
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from footballfantasyapi import crud
from footballfantasyapi import schemas
from footballfantasyapi.api import deps
from footballfantasyapi.models.user import User
from footballfantasyapi.core.auth import authenticate, create_access_token
from footballfantasyapi.clients.base_team_generator import BaseTeamGeneratorClient

router = APIRouter()


@router.post("/login")
def login(
        db: Session = Depends(deps.get_db),
        form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    Get the JWT for a user with data from OAuth2 request form body.
    """

    user = authenticate(email=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {
        "access_token": create_access_token(sub=str(user.id)),
        "token_type": "bearer",
    }


@router.get("/profile", response_model=schemas.Profile)
def read_user_profile(
        *,
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_user)) -> schemas.Profile:
    """
    Fetch the current logged in user.
    """
    return crud.user.get_profile(db=db, user_id=current_user.id)


@router.post("/signup", response_model=schemas.Profile, status_code=201)
def create_user_signup(
        *,
        db: Session = Depends(deps.get_db),
        user_in: schemas.user.UserCreate,
        team_client: BaseTeamGeneratorClient = Depends(deps.get_team_generator_client)) -> Any:
    """
    Create new user without the need to be logged in.
    """

    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user = crud.user.create(db=db, obj_in=user_in)

    team_in: schemas.TeamCreate = team_client.generate_team(user_id=user.id)
    team: schemas.Team = crud.team.create(db=db, obj_in=team_in)

    players_in: Sequence[schemas.PlayerCreate] = team_client.generate_players(team_id=team.id)
    players: List[schemas.Player] = []
    for player_in in players_in:
        player: schemas.Player = crud.player.create(db=db, obj_in=player_in)
        players.append(player)

    return crud.user.get_profile(db=db, user_id=user.id)
