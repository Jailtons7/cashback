import os
from pathlib import Path
from environs import Env

env = Env()
env.read_env()


class Settings:
    SECRET_KEY = env.str("SECRET_KEY")

    PROJECT_ROOT = Path(__file__).parent.parent
    FLASK_RUN_HOST = env.str("FLASK_RUN_HOST")
    FLASK_RUN_PORT = env.int("FLASK_RUN_PORT")
    FLASK_DEBUG = env.bool("FLASK_DEBUG")
