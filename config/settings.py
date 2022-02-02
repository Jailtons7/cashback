from urllib.parse import quote_plus
from environs import Env

env = Env()
env.read_env()


class Settings:
    SECRET_KEY = env.str("SECRET_KEY")

    DEBUG = env.bool("DEBUG")
    PAGINATION = env.int("PAGINATION", 10)

    DB = env.str("DB")
    DB_USER = env.str("DB_USER")
    DB_PASSWORD = env.str("DB_PASSWORD")

    MONGODB_SETTINGS = {
        'host': env.str("DB_HOST").format(user=quote_plus(DB_USER), pwd=quote_plus(DB_PASSWORD), db=quote_plus(DB)),
    }
    JWT_SECRET_KEY = SECRET_KEY
