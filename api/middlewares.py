from flask import request, jsonify, g

from api import app
from api.authentication.models import User


@app.before_request
def verify_headers_middleware():
    """
    Middleware to return BAD REQUEST if user
    call a POST without specify content-type as application/json
    """
    required = [
        request.method == 'POST',
        request.headers.get('Content-Type') != 'application/json'
    ]
    if all(required):
        return jsonify({'msg': 'Content-Type wrong or not set.'}), 400


def user_view(_jwt_header, jwt_data):
    """
    Stores user into g.user before any authenticated request
    """
    identity = jwt_data['sub']
    user = User.objects(email=identity).first()
    g.user = user
    return user
