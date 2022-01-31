import pytest

from flask_mongoengine import MongoEngine

from api import app, db
from config.settings import Settings

db.disconnect()


class TestSettings(Settings):
    TESTING = True
    MONGODB_SETTINGS = {
        'db': 'test',
        'host': 'mongodb://127.0.0.1:5000/test',
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
            db.connection.drop_database('test')
