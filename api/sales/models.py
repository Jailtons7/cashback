import re

from mongoengine.errors import ValidationError

from api import db


class Purchase(db.Document):
    code = db.StringField(required=True, unique=True)
    cpf = db.StringField(required=True, max_length=11)
    value = db.DecimalField(required=True, precision=2)
    date = db.DateField(required=True)
    status = db.StringField(default="Em validação")
    cashback_percent = db.DecimalField(precision=2)
    cashback_value = db.DecimalField(precision=2)

    def __init__(self, code, cpf, value, date, *args, **kwargs):
        super(Purchase, self).__init__(*args, **kwargs)
        self.code = code
        self.cpf = cpf
        self.value = value
        self.date = date

    def __str__(self):
        return f'Compra {self.code}'

    def __repr__(self):
        return f'<Purchase {self.code}>'

    def clean(self) -> None:
        """
        Ensures that cpf has only 11 numbers and set cashback_percent and cashback_value
        """
        pattern = r'\d{11}'
        if not bool(re.match(pattern, self.cpf)):
            raise ValidationError('cpf field must have only 11 numbers.')

        if self.cpf == '15350946056':
            self.status = 'Aprovado'

        if self.value <= 1000.0:
            self.cashback_percent = 0.1
        elif self.value <= 1500.0:
            self.cashback_percent = 0.15
        else:
            self.cashback_percent = 0.2

        self.cashback_value = self.value * self.cashback_percent

    @staticmethod
    def required_fields():
        return 'fields code, cpf, value and date are required'
