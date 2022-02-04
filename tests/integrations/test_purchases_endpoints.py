import json

from api.sales.models import Purchase


mimetype = 'application/json'
headers = {
    'Content-Type': mimetype,
    'Accept': mimetype
}


def get_token(client):
    auth_dict = {
        'email': 'user1@example.com',
        'password': 'password.@'
    }
    req = client.post('/authentication/create-token', data=json.dumps(auth_dict), headers=headers)
    return req.json['access_token']


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
    headers['Authorization'] = f'Bearer {get_token(client)}'
    req = client.post("/purchases", data=json.dumps(purchase_data), headers=headers)
    assert req.status_code == 201
    assert req.json["msg"] == "Successfully added"
    assert all([key in req.json["data"] for key in purchase_data.keys()])
    assert all([value == req.json["data"][key] for key, value in purchase_data.items() if key != 'date'])


def test_purchase_code_exists_fail(client, normal_user):
    """
    GIVEN a POST to '/purchases' endpoint
    WHEN the purchase code already exists
    THEN check the status code and message of response
    """
    purchase_data = {
        "code": "3000",
        "cpf": "12312312312",
        "value": 722.89,
        "date": "2022-01-01"
    }
    headers['Authorization'] = f'Bearer {get_token(client)}'
    req = client.post("/purchases", data=json.dumps(purchase_data), headers=headers)
    assert req.status_code == 400
    assert req.json["msg"] == f"There's already a purchase with code '{purchase_data['code']}'"


def test_purchase_required_fields(client, normal_user):
    """
    GIVEN a POST to '/purchases' endpoint
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
    headers['Authorization'] = f'Bearer {get_token(client)}'
    keys = ["code", "cpf", "value", "date"]
    for key in keys:
        del purchase_data[key]
        req = client.post("/purchases", data=json.dumps(purchase_data), headers=headers)
        assert req.status_code == 400
        assert req.json["msg"] == Purchase.required_fields()
        purchase_data = fixed_dict.copy()


def test_purchases_response_cpf_validation(client, normal_user):
    """
    GIVEN a POST to '/purchases' endpoint
    WHEN the purchase to be created has invalid cpf
    THEN check the status code and message
    """
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
