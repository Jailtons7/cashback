from api import app, jwt
from api.authentication import views
from api.middlewares import user_view


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    return user_view(_jwt_header, jwt_data)


@app.route('/authentication/create-token', methods=['POST'], strict_slashes=False)
def login():
    return views.create_token()


@app.route('/authentication/users', methods=['GET', 'POST', 'PUT', 'DELETE'], strict_slashes=False)
def users():
    return views.users_view()
