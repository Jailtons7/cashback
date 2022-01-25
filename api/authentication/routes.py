from api import app
from api.authentication import views


@app.route('/authentication/create-token', methods=['POST'], strict_slashes=False)
def login():
    return views.create_token()


@app.route('/authentication/users', methods=['GET', 'POST', 'PUT', 'DELETE'], strict_slashes=False)
def users():
    return views.users_view()
