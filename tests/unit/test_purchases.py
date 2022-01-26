from datetime import date

import pytest

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


def test_purchase_save():
    """
    GIVEN a Purchase model
    WHEN a new instance of Purchase is created
    THEN check the code, cpf, value and date fields
    """
