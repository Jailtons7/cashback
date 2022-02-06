from flask import Flask, jsonify

from config.settings import Settings
from extensions.jwt import init_jwt
from extensions.db import init_db
from extensions.bcript import init_bcript
from api.authentication.routes import user_blueprint
from api.sales.routes import sales_blueprint
from api.middlewares import breq_blueprint, user_view


def create_app(from_config=Settings):
    app = Flask(__name__)
    app.config.from_object(from_config)

    bcript = init_bcript()
    bcript.init_app(app=app)

    db = init_db()
    db.init_app(app=app)

    jwt = init_jwt()
    jwt.init_app(app=app)

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        return user_view(_jwt_header, jwt_data)

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
            "code": "See code at https://github.com/Jailtons7/cashback"
        })

    app.register_blueprint(breq_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(sales_blueprint)
    return app
