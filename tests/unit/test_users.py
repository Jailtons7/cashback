import pytest
from mongoengine.errors import ValidationError, NotUniqueError

from api.authentication.models import User


def test_user_instance():
    """
    GIVEN a User model
    WHEN a new instance of User is created
    THEN check the nome, cpf, email and password fields
    """
    user = User(nome='josé', cpf='12345678912', email='jose@gmail.com')
    user.set_password('my-secret.@')

    assert user.nome == 'josé'
    assert user.cpf == '12345678912'
    assert user.email == 'jose@gmail.com'
    assert user.password != 'my-secret.@'


def test_required_fields():
    assert User.required_fields() == 'fields nome, cpf email and password are required'
    assert User.unique_fields() == "There's already an account with the given cpf or email."


def test_user_save(client):
    """
    GIVEN a User instance
    WHEN the save method is called
    THEN check the instance is saved
    """
    user = User(nome='josé', cpf='12345678912', email='jose@gmail.com')

    with pytest.raises(ValidationError):
        assert user.save()

    user.set_password('my-secret.@')
    usr = user.save()
    assert usr is not None


def test_user_already_exists(client):
    """
    GIVEN a User instance
    WHEN the cpf or email already exists
    THEN check if raises NotUniqueError
    """
    user1 = User(nome='josé', cpf='12345678912', email='jose@gmail.com')
    user2 = User(nome='maria', cpf='12345678912', email='maria@gmail.com')
    user3 = User(nome='josé2', cpf='98765432198', email='jose@gmail.com')

    user1.set_password('my-secret.@')
    user2.set_password('my-secret.@')
    user3.set_password('my-secret.@')

    with pytest.raises(NotUniqueError):
        assert user1.save()
        assert user2.save()
        assert user3.save()


def test_cpf_validation():
    """
    GIVEN a User instance
    WHEN an invalid cpf is given
    THEN check if raises ValidationError
    """
    user1 = User(nome='user', cpf='123.123.123.-12', email='user@gmail.com')
    user2 = User(nome='user', cpf='123123123a2', email='user@gmail.com')
    user3 = User(nome='user', cpf='1231231232', email='user@gmail.com')

    user1.set_password('my-secret.@')
    user2.set_password('my-secret.@')
    user3.set_password('my-secret.@')

    with pytest.raises(ValidationError):
        assert user1.save()
        assert user2.save()
        assert user3.save()
