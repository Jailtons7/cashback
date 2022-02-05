import pytest

from environs import Env
from flask_mongoengine import MongoEngine

from api import create_app
from extensions.db import init_db
from api.authentication.models import User
from config.settings import TestSettings


db = init_db()
db.disconnect()

env = Env()
env.read_env()


app = create_app(from_config=TestSettings)


@pytest.fixture(scope="session")
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


@pytest.fixture(scope="session")
def normal_user():
    n_user = User(nome='user1', email='user1@example.com', cpf='12345678987')
    n_user.set_password('password.@')
    n_user.save()
    return n_user


@pytest.fixture(scope="session")
def approved_user():
    a_user = User(nome='user2', email='user2@example.com', cpf='15350946056')
    a_user.set_password('password.@')
    a_user.save()
    return a_user
