import logging
from sqlalchemy.orm import Session

from footballfantasyapi.db import base  # noqa: F401
from footballfantasyapi import crud, schemas

logger = logging.getLogger(__name__)

FIRST_SUPERUSER = "admin@teamapi.com"


# make sure all SQL Alchemy models are imported (footballfantasyapi.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # return
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    # if FIRST_SUPERUSER:
    #     user = crud.user.get_by_email(db, email=FIRST_SUPERUSER)
    #     if not user:
    #         user_in = schemas.UserCreate(
    #             email=FIRST_SUPERUSER,
    #         )
    #         user = crud.user.create(db, obj_in=user_in)  # noqa: F841
    #     else:
    #         logger.warning(
    #             "Skipping creating superuser. User with email "
    #             f"{FIRST_SUPERUSER} already exists. "
    #         )
    #     if not user.teams:
    #         for team in TEAMS:
    #             team_in = schemas.TeamCreate(
    #                 name=team['name'],
    #                 country=team['country'],
    #                 value=team['value'],
    #                 funds=team['funds'],
    #                 user_id=user.id,
    #             )
    #             crud.team.create(db, obj_in=team_in)
    # else:
    #     logger.warning(
    #         "Skipping creating superuser.  FIRST_SUPERUSER needs to be "
    #         "provided as an env variable. "
    #         "e.g.  FIRST_SUPERUSER=admin@api.coursemaker.io"
    #     )
    pass
