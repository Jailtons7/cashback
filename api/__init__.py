from flask import Flask, jsonify
from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, current_user, jwt_required, JWTManager

from config.settings import Settings


app = Flask(__name__)
app.config.from_object(Settings)

bcript = Bcrypt(app=app)
db = MongoEngine(app=app)
jwt = JWTManager(app=app)


@app.get('/')
def index():
    return jsonify({
        "msg": "Welcome to Boticario's Cashback API",
        "routes": {
            "authentication": [
                {
                    "endpoint": "/authentication/users",
                    "methods": ["POST"]
                },
                {
                    "endpoint": "/authentication/create-token",
                    "methods": ["POST"]
                }
            ],
            "sales": [
                {
                    "endpoint": "/purchases",
                    "methods": ["GET", "POST"]
                },
                {
                    "endpoint": "/cashback/<string:cpf>",
                    "methods": ["GET"]
                }
            ]
        },
        "code": "See code at https://github.com/Jailtons7/cashback",
        "test": "test CI/CD"
    })


from config import routes
