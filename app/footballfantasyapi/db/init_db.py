import logging
from typing import Sequence, List
from sqlalchemy.orm import Session

from app.footballfantasyapi.api import deps
from app.footballfantasyapi.db import base  # noqa: F401
from app.footballfantasyapi import crud, schemas
from app.footballfantasyapi.core.config import settings
from app.footballfantasyapi.clients.base_team_generator import BaseTeamGeneratorClient

logger = logging.getLogger(__name__)

FIRST_SUPERUSER = "admin@teamapi.com"


# make sure all SQL Alchemy models are imported (footballfantasyapi.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session,
            team_client: BaseTeamGeneratorClient = deps.get_team_generator_client()) -> None:
    if settings.FIRST_SUPERUSER:
        user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
        if not user:
            user_in = schemas.UserCreate(
                full_name="Initial Super User",
                email=settings.FIRST_SUPERUSER,
                is_superuser=True,
                password=settings.FIRST_SUPERUSER_PW,
            )
            user = crud.user.create(db, obj_in=user_in)  # noqa: F841
        else:
            logger.warning(
                "Skipping creating superuser. User with email "
                f"{settings.FIRST_SUPERUSER} already exists. "
            )
        if not user.teams:
            team_in: schemas.TeamCreate = team_client.generate_team(user_id=user.id)
            team: schemas.Team = crud.team.create(db=db, obj_in=team_in)
            players_in: Sequence[schemas.PlayerCreate] = team_client.generate_players(team_id=team.id)
            players: List[schemas.Player] = []
            for player_in in players_in:
                player: schemas.Player = crud.player.create(db=db, obj_in=player_in)
                players.append(player)

    else:
        logger.warning(
            "Skipping creating superuser.  FIRST_SUPERUSER needs to be "
            "provided as an env variable. "
            "e.g.  FIRST_SUPERUSER=admin@api.coursemaker.io"
        )
