from flask import request, jsonify
from flask_jwt_extended import create_access_token

from api.authentication.models import Revendedor


def create_token():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    revendedor = Revendedor.objects(email=email).first()
    print(revendedor)
    if revendedor.verify_password(password):
        return jsonify({
            'access_token': create_access_token(identity=email)
        })
    return jsonify({
        'msg': 'No active account with the given credentials'
    }), 401


def users_view(id=None):
    if request.method == 'POST':
        data = request.json

        try:
            rev = Revendedor(**data)
        except TypeError as e:
            print(e)
            return jsonify({'msg': Revendedor.required_fields()}), 400

        try:
            rev.save()
        except Exception as e:
            print(e)
            return jsonify({'msg': ''}), 400

        return jsonify({
            'msg': 'succeesfuly added',
            'data': rev
        }), 201
