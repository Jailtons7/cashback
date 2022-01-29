from flask import request, jsonify
from flask_jwt_extended import create_access_token
from mongoengine.errors import NotUniqueError

from api.authentication.models import User


def create_token():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    user = User.objects(email=email).first()
    if user and user.verify_password(password):
        return jsonify({
            'access_token': create_access_token(identity=email)
        }), 201
    return jsonify({
        'msg': 'No active account with the given credentials'
    }), 401


def users_view(id=None):
    if request.method == 'POST':
        data = request.json

        if not data['password']:
            return jsonify({'msg': User.required_fields()}), 400

        try:
            user = User(**data)
        except TypeError as e:
            print(e)
            return jsonify({'msg': User.required_fields()}), 400

        try:
            user.set_password(data['password'])
            user.save()
        except NotUniqueError as e:
            print(e)
            return jsonify({'msg': User.unique_fields()}), 400

        return jsonify({
            'msg': 'successfuly added',
            'data': user
        }), 201
