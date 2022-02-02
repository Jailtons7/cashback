import pytest
from urllib.parse import quote_plus

from environs import Env
from flask_mongoengine import MongoEngine

from api import app, db
from config.settings import Settings

db.disconnect()
env = Env()
env.read_env()


class TestSettings(Settings):
    TESTING = True
    DB = env.str('DB_TEST', 'test')
    DB_USER = env.str("DB_USER")
    DB_PASSWORD = env.str("DB_PASSWORD")

    MONGODB_SETTINGS = {
        'host': 'mongodb+srv://{user}:{pwd}@cluster0.yuhnh.mongodb.net/{db}?retryWrites=true&w=majority'.format(
            user=quote_plus(DB_USER), pwd=quote_plus(DB_PASSWORD), db=quote_plus(DB)
        ),
    }


@pytest.fixture(scope="module")
def client():
    app.config.from_object(TestSettings)
    with app.test_client() as client:
        with app.app_context():
            # Inicia uma conexão com o db de testes
            db = MongoEngine(app)

        yield client  # Realiza os testes

        with app.app_context():
            # Apaga o db de testes
            db.connection.drop_database(TestSettings.DB)
