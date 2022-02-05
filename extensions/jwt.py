from flask_jwt_extended import JWTManager


def init_jwt():
    jwt = JWTManager()
    return jwt
