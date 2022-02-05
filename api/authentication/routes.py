from flask import Blueprint

from extensions.jwt import init_jwt
from api.authentication import views

jwt = init_jwt()

user_blueprint = Blueprint('user_blueprint', __name__)


@user_blueprint.route('/authentication/create-token', methods=['POST'], strict_slashes=False)
def login():
    return views.create_token()


@user_blueprint.route('/authentication/users', methods=['GET', 'POST', 'PUT', 'DELETE'], strict_slashes=False)
def users():
    return views.users_view()
