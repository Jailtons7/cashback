from flask import Flask
from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, current_user, jwt_required, JWTManager

from config.settings import Settings


app = Flask(__name__)
app.config.from_object(Settings)

bcript = Bcrypt(app=app)
db = MongoEngine(app=app)
jwt = JWTManager(app=app)

from config import routes
