# Import all the models, so that Base has them before being
# imported by Alembic
from app.footballfantasyapi.db.base_class import Base  # noqa
from app.footballfantasyapi.models.user import User  # noqa
from app.footballfantasyapi.models.team import Team  # noqa
from app.footballfantasyapi.models.player import Player  # noqa
