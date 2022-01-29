import json

from api.authentication.models import User


mimetype = 'application/json'
headers = {
    'Content-Type': mimetype,
    'Accept': mimetype
}


def test_create_user(client):
    """
    GIVEN the /authentication/users endpoint
    WHEN a POST request is made
    THEN check the status code, message and data of response
    """
    usr_data = {
        "nome": "ana",
        "cpf": "12345678913",
        "email": "ana@gmail.com",
        "password": "my-secret.@"
    }
    req = client.post('http://localhost:5000/authentication/users', data=json.dumps(usr_data), headers=headers)
    assert req.status == '201 CREATED'
    assert req.json['msg'] == 'successfuly added'
    assert all([key in req.json['data'] for key in usr_data.keys()])


def test_get_token(client):
    """
    GIVEN the /authentication/users endpoint
    WHEN a POST request is made
    THEN check the status code, message and data of response
    """
    usr_data = {
        "nome": "user",
        "cpf": "98765432198",
        "email": "user@example.com",
    }
    login = {
        'email': usr_data['email'],
        'password': 'my-secret.@'
    }
    user = User(**usr_data)
    user.set_password('my-secret.@')
    user.save()
    req = client.post('/authentication/create-token')
    assert req.status_code == 400

    req2 = client.post('/authentication/create-token', data=json.dumps(login), headers=headers)
    assert req2.status_code == 201
    assert 'access_token' in req2.json

