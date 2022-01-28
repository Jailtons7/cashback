from environs import Env

env = Env()
env.read_env()


class Settings:
    SECRET_KEY = env.str("SECRET_KEY")

    DEBUG = env.bool("DEBUG")
    PAGINATION = env.int("PAGINATION", 10)

    MONGODB_SETTINGS = {
        'host': env.str("DB_HOST"),
    }
    JWT_SECRET_KEY = SECRET_KEY
