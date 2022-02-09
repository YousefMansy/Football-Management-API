# Import all the models, so that Base has them before being
# imported by Alembic
from footballfantasyapi.db.base_class import Base  # noqa
from footballfantasyapi.models.user import User  # noqa
from footballfantasyapi.models.team import Team  # noqa
from footballfantasyapi.models.player import Player  # noqa
