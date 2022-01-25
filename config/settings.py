import os
from pathlib import Path
from environs import Env

env = Env()
env.read_env()


class Settings:
    SECRET_KEY = env.str("SECRET_KEY")

    APPLICATION_ROOT = Path(__file__).parent.parent
    HOST = env.str("RUN_HOST")
    FLASK_RUN_PORT = env.int("FLASK_RUN_PORT")
    DEBUG = env.bool("DEBUG")
    PAGINATION = env.int("PAGINATION", 10)

    MONGODB_SETTINGS = {
        'db': env.str("DB"),
        'host': env.str("DB_HOST"),
    }
    JWT_SECRET_KEY = SECRET_KEY
