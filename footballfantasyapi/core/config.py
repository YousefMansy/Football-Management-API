from typing import List, Optional, Union
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    JWT_SECRET: str = "DEV_SECRET"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000",
    # "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    SQLALCHEMY_DATABASE_URI: Optional[str] = "sqlite:///example2.db"
    FIRST_SUPERUSER: EmailStr = "admin@recipeapi.com"
    INITIAL_PLAYER_VALUE: int = 1000000
    INITIAL_TEAM_FUNDS: int = 5000000
    INITIAL_TEAM_STRUCTURE: dict = {
        'GK': 3,
        'DF': 6,
        'MF': 6,
        'AT': 5
    }
    INITIAL_PLAYERS_COUNT: int = sum(INITIAL_TEAM_STRUCTURE.values())
    MIN_PLAYER_AGE: int = 18
    MAX_PLAYER_AGE: int = 40

    class Config:
        env_file = '.env'
        case_sensitive = True


settings = Settings()
