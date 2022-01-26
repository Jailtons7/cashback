import re

from mongoengine.errors import ValidationError

from api import db, bcript


class User(db.Document):
    nome = db.StringField(required=True, max_length=150)
    cpf = db.StringField(required=True, max_length=11, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)

    def __init__(self, nome, cpf, email, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nome = nome
        self.cpf = cpf
        self.email = email

    def __repr__(self):
        return f'<User {self.nome}>'

    def __str__(self):
        return f'<User {self.nome}>'

    def clean(self) -> None:
        """
        Ensures that cpf has only 11 numbers and set cashback_percent and cashback_value
        """
        pattern = r'\d{11}'
        if not bool(re.match(pattern, self.cpf)):
            raise ValidationError('cpf field must have only 11 numbers.')

    def set_password(self, password):
        self.password = bcript.generate_password_hash(password).decode('utf-8')

    def verify_password(self, pwd):
        return bcript.check_password_hash(self.password, pwd)

    @staticmethod
    def required_fields():
        return 'fields nome, cpf email and password are required'

    @staticmethod
    def unique_fields():
        return "There's already an account with the given cpf or email."
