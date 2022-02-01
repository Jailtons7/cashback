import re
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

from mongoengine.errors import ValidationError
from mongoengine.queryset.visitor import Q

from api import db
from api.authentication.models import User


class Purchase(db.Document):
    user = db.ReferenceField(User, required=True)
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

    def set_user(self, user):
        self.user = user

    def clean(self) -> None:
        """
        Ensures that cpf has only 11 numbers and set cashback_percent and cashback_value
        """
        pattern = r'\d{11}'
        if not bool(re.match(pattern, self.cpf)):
            raise ValidationError('cpf field must have only 11 numbers.')

        if self.user.cpf == '15350946056':
            self.status = 'Aprovado'

        self.cashback_percent = self.cashback_decimal(self.value)
        self.cashback_value = self.value * self.cashback_percent

    @staticmethod
    def required_fields():
        return 'fields code, cpf, value and date are required'

    @classmethod
    def get_monthly_cashback(cls, cpf):
        """
        Returns the cashback of a given buyer
        """
        today = date.today()
        prev_month = today + relativedelta(months=-1)
        purchases = cls.objects(cpf=cpf, status="Aprovado")
        prev_purchases = purchases.filter(
            (Q(date__gte=date(prev_month.year, prev_month.month, 1)) & Q(date__lte=prev_month))
        )
        tot_value = sum([purchase.value for purchase in prev_purchases])
        return round(float(tot_value) * cls.cashback_decimal(tot_value), 2)

    @staticmethod
    def cashback_decimal(value):
        if value <= 1000.0:
            return 0.1
        elif value <= 1500.0:
            return 0.15
        else:
            return 0.2
