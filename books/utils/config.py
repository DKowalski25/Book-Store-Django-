import os

from typing import Final
from dotenv import load_dotenv

from utils.exceptions.configurate_exeptions import EnvDependNotFound

load_dotenv()


def get_env_var(var_name: str) -> str:
    value: str | None = os.getenv(var_name)
    if value is None:
        raise EnvDependNotFound
    else:
        return value


NAME_DB_POSTGRESQL: Final[str] = get_env_var('NAME_DB_POSTGRESQL')
USER_DB_POSTGRESQL: Final[str] = get_env_var('USER_DB_POSTGRESQL')
PASSWORD_DB_POSTGRESQL: Final[str] = get_env_var('PASSWORD_DB_POSTGRESQL')
HOST_DB_POSTGRESQL: Final[str] = get_env_var('HOST_DB_POSTGRESQL')
PORT_DB_POSTGRESQL: Final[str] = get_env_var('PORT_DB_POSTGRESQL')
SECRET_KEY: Final[str] = get_env_var('SECRET_KEY')
SOCIAL_AUTH_GITHUB_KEY: Final[str] = get_env_var('SOCIAL_AUTH_GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET: Final[str] = get_env_var('SOCIAL_AUTH_GITHUB_SECRET')
