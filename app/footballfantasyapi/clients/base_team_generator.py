from typing import Sequence

from app.footballfantasyapi import schemas
from app.footballfantasyapi.clients import utils
from app.footballfantasyapi.core.config import settings


class BaseTeamGeneratorClient:

    def generate_team(self, user_id: int) -> schemas.TeamCreate:
        team_in: schemas.TeamCreate = schemas.TeamCreate(
            name=utils.generate_team_name(),
            country=utils.generate_country(),
            value=settings.INITIAL_PLAYER_VALUE * settings.INITIAL_PLAYERS_COUNT,
            funds=settings.INITIAL_TEAM_FUNDS,
            user_id=user_id
        )
        return team_in

    def generate_player(self, pos: str, team_id: int) -> schemas.PlayerCreate:
        return schemas.PlayerCreate(
            first_name=utils.generate_first_name(),
            last_name=utils.generate_last_name(),
            country=utils.generate_country(),
            age=utils.generate_age(),
            position=pos,
            market_value=settings.INITIAL_PLAYER_VALUE,
            team_id=team_id
        )

    def generate_players(self, team_id: int) -> Sequence[schemas.PlayerCreate]:
        players_in = []
        for pos, value in settings.INITIAL_TEAM_STRUCTURE.items():
            for i in range(value):
                players_in.append(self.generate_player(pos, team_id))
        return players_in
