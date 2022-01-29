from datetime import date

import pytest
from mongoengine.errors import ValidationError, NotUniqueError

from api.sales.models import Purchase


def test_purchase_instance():
    """
    GIVEN a Purchase model
    WHEN a new instance of Purchase is created
    THEN check the code, cpf, value and date fields
    """
    dt = date.today()
    purchase = Purchase(code='1', cpf='12345678912', value=750, date=dt)
    assert purchase.code == '1'
    assert purchase.cpf == '12345678912'
    assert purchase.value == 750
    assert purchase.date == dt


def test_required_fields():
    assert Purchase.required_fields() == 'fields code, cpf, value and date are required'


def test_purchase_save(client):
    """
    GIVEN a Purchase model
    WHEN a new instance of Purchase is created
    THEN check the code, cpf, value and date fields
    """
    dt = date.today()
    purchase = Purchase(code='1', cpf='12345678912', value=750, date=dt)
    assert purchase.cashback_percent is None
    assert purchase.cashback_value is None

    obj = purchase.save()

    assert obj is not None
    assert obj.cashback_percent == 0.1
    assert obj.cashback_value == 75.0


def test_not_unique():
    """
    GIVEN a saved Purchase
    WHEN a new instance of Purchase is saved with the same code
    THEN check NotUniqueError
    """
    purchase1 = Purchase(code='1000', cpf='12345678912', value=2000, date=date.today()).save()
    purchase2 = Purchase(code='1000', cpf='12345678912', value=5000, date=date.today())
    with pytest.raises(NotUniqueError):
        purchase2.save()


def test_cpf_validation():
    """
    GIVEN a Purchase instance
    WHEN an invalid cpf is given
    THEN check if raises ValidationError
    """
    dt = date.today()
    purchase = Purchase(code='1', cpf='123.123.123.-12', value=750, date=dt)
    purchase2 = Purchase(code='1', cpf='123123123a2', value=750, date=dt)
    purchase3 = Purchase(code='1', cpf='1231231232', value=750, date=dt)

    with pytest.raises(ValidationError):
        purchase.save()
    with pytest.raises(ValidationError):
        purchase2.save()
    with pytest.raises(ValidationError):
        purchase3.save()


def test_cashback_percent():
    """
    GIVEN a Purchase instance
    WHEN a value is given
    THEN check the cashback percent
    """
    dt = date.today()
    purchase = Purchase(code='2', cpf='12312312312', value=750, date=dt)
    purchase2 = Purchase(code='3', cpf='12312312312', value=1150, date=dt)
    purchase3 = Purchase(code='4', cpf='12312312312', value=2050, date=dt)
    purchase.save()
    purchase2.save()
    purchase3.save()

    assert purchase.cashback_percent == 0.1
    assert purchase2.cashback_percent == 0.15
    assert purchase3.cashback_percent == 0.2


def test_cashback_value():
    """
    GIVEN a Purchase instance
    WHEN a value is given
    THEN check the cashback percent
    """
    dt = date.today()
    purchase = Purchase(code='5', cpf='12312312312', value=750, date=dt).save()
    purchase2 = Purchase(code='6', cpf='12312312312', value=1150, date=dt).save()
    purchase3 = Purchase(code='7', cpf='12312312312', value=2050, date=dt).save()

    assert purchase.cashback_value == 75.0
    assert purchase2.cashback_value == 172.5
    assert purchase3.cashback_value == 410.0


def test_cashback_status():
    """
    GIVEN a Purchase instance
    WHEN a cpf is given
    THEN check the purschase status
    """
    purchase = Purchase(code='8', cpf='12312312312', value=750, date=date.today()).save()
    assert purchase.status == 'Em validação'
    purchase = Purchase(code='9', cpf='15350946056', value=750, date=date.today()).save()
    assert purchase.status == 'Aprovado'
