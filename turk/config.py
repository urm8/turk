"""setup project."""
import os
from typing import Mapping

import dotenv
from tortoise import Tortoise

dotenv.load_dotenv()

db_uri = os.environ['DB_URI']
api_key = os.environ['KEY']

TORTOISE_ORM: Mapping = {  # noqa: WPS407
    'connections': {'default': db_uri},
    'apps': {
        'models': {
            'models': ['turk.models', 'aerich.models'],
            'default_connection': 'default',
        },
    },
}


async def init_db():
    """Initialize database connection."""
    await Tortoise.init(TORTOISE_ORM)
