import names
import random
import pycountry
import randomname

from footballfantasyapi.core.config import settings


def generate_team_name() -> str:
    return ' '.join(word.title() for word in randomname.generate(('adj/speed', 'adj/size', 'adj/appearance'),
                                                                 ('nouns/sports', 'nouns/ghosts')).split('-'))


def generate_country() -> str:
    return random.choice(list(pycountry.countries)).name


def generate_first_name() -> str:
    return names.get_first_name()


def generate_last_name() -> str:
    return names.get_last_name()


def generate_age() -> int:
    return random.randint(settings.MIN_PLAYER_AGE, settings.MAX_PLAYER_AGE)
