import json
from datetime import date

from dateutil.relativedelta import relativedelta

from api.sales.models import Purchase
from integrations.boticario import BoticarioCashback


mimetype = 'application/json'
headers = {
    'Content-Type': mimetype,
    'Accept': mimetype
}

normal_user_credentials = {
    'email': 'user1@example.com',
    'password': 'password.@'
}
approved_user_credentials = {
    'email': 'user2@example.com',
    'password': 'password.@'
}


def get_token(client, auth_dict):
    """
    returns access token from user,
    only call this function if your test uses either normal_user or approved_user fixture
    """
    req = client.post('/authentication/create-token', data=json.dumps(auth_dict), headers=headers)
    return req.json['access_token']


def test_retrieve_purchases(client, normal_user):
    """
    GIVEN a GET request to '/purchases' endpoint
    WHEN purchases are in database
    THEN check the status code, message and the response data
    """
    headers['Authorization'] = f'Bearer {get_token(client, normal_user_credentials)}'
    req = client.get('/purchases', headers=headers)
    assert req.status_code == 200
    assert req.json['msg'] == 'Successfully fetched'
    assert req.json['total'] == 0
    assert req.json['data'] == []

    # Save some purchases
    today = date.today()
    dict_purchases = [
        dict(code='1700', cpf='12345678912', value=750, date=today),
        dict(code='5700', cpf='12345678912', value=1750, date=today),
        dict(code='6700', cpf='12345678912', value=2750, date=today),
        dict(code='2700', cpf='12345678912', value=450, date=today),
    ]
    for purc in dict_purchases:
        purchase = Purchase(**purc)
        purchase.set_user(normal_user)
        purchase.save()

    req = client.get('/purchases', headers=headers)
    assert req.status_code == 200
    assert req.json['msg'] == 'Successfully fetched'
    assert req.json['total'] == 4
    assert len(req.json['data']) == 4


def test_add_purchase(client, normal_user):
    """
    GIVEN the /purchases endpoint
    WHEN a POST request is made
    THEN check the status code, message and data of response
    """
    purchase_data = {
        "code": "3000",
        "cpf": "12312312312",
        "value": 722.89,
        "date": "2022-01-01"
    }
    headers['Authorization'] = f'Bearer {get_token(client, normal_user_credentials)}'
    req = client.post("/purchases", data=json.dumps(purchase_data), headers=headers)
    assert req.status_code == 201
    assert req.json["msg"] == "Successfully added"
    assert all([key in req.json["data"] for key in purchase_data.keys()])
    assert all([value == req.json["data"][key] for key, value in purchase_data.items() if key != 'date'])


def test_purchase_code_exists_fail(client, normal_user):
    """
    GIVEN a POST request to '/purchases' endpoint
    WHEN the purchase code already exists
    THEN check the status code and message of response
    """
    purchase_data = {
        "code": "3000",
        "cpf": "12312312312",
        "value": 722.89,
        "date": "2022-01-01"
    }
    headers['Authorization'] = f'Bearer {get_token(client, normal_user_credentials)}'
    req = client.post("/purchases", data=json.dumps(purchase_data), headers=headers)
    assert req.status_code == 400
    assert req.json["msg"] == f"There's already a purchase with code '{purchase_data['code']}'"


def test_purchase_required_fields(client, normal_user):
    """
    GIVEN a POST request to '/purchases' endpoint
    WHEN the purchase to be created is invalid
    THEN check the status code and message
    """
    purchase_data = {
        "code": "3000",
        "cpf": "12312312312",
        "value": 722.89,
        "date": "2022-01-01"
    }
    fixed_dict = purchase_data.copy()
    headers['Authorization'] = f'Bearer {get_token(client, normal_user_credentials)}'
    keys = ["code", "cpf", "value", "date"]
    for key in keys:
        del purchase_data[key]
        req = client.post("/purchases", data=json.dumps(purchase_data), headers=headers)
        assert req.status_code == 400
        assert req.json["msg"] == Purchase.required_fields()
        purchase_data = fixed_dict.copy()


def test_purchases_response_cpf_validation(client, normal_user):
    """
    GIVEN a POST request to '/purchases' endpoint
    WHEN the purchase to be created has invalid cpf
    THEN check the status code and message
    """
    headers["Authorization"] = f"Bearer {get_token(client, normal_user_credentials)}"
    cpfs = ['123.123.123-12', '123123123 12', '123123123as', '1231231', 'asdasdasdas']
    for cpf in cpfs:
        purchase_data = {
            "code": "5000",
            "cpf": cpf,
            "value": 722.89,
            "date": "2022-01-01"
        }
        req = client.post("/purchases", data=json.dumps(purchase_data), headers=headers)
        assert req.status_code == 400
        assert "cpf field must have only 11 numbers" in req.json["msg"]


def test_get_cashback(client, approved_user):
    """
    GIVEN a GET request to '/cashback/<str:cpf>' endpoint
    WHEN the given cpf have made purchases in the previous month
    THEN check the total cashback
    """
    headers['Authorization'] = f'Bearer {get_token(client, approved_user_credentials)}'
    req = client.get("/cashback/98765432123", headers=headers)
    assert req.status_code == 200
    assert req.json['msg'] == 'Successfully fetched'
    assert "cashback" in req.json

    today = date.today()
    prev_month = today + relativedelta(months=-1)

    purchases = [
        dict(code='1800', cpf='98765432123', value=750, date=prev_month),
        dict(code='5800', cpf='98765432123', value=1750, date=prev_month),
        dict(code='6800', cpf='98765432123', value=2750, date=prev_month),
        dict(code='2800', cpf='98765432123', value=450, date=prev_month),
    ]
    boticario_credit = BoticarioCashback.get_boticario_credits(cpf='98765432123')
    for purc in purchases:
        purchase = Purchase(**purc)
        purchase.set_user(approved_user)
        purchase.save()
        req = client.get("/cashback/98765432123", headers=headers)

    assert req.json["cashback"] == 5700 * Purchase.cashback_decimal(5700) + boticario_credit
