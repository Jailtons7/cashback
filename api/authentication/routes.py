from api import app
from api.authentication import views


@app.route('/authentication/crete-token', methods=['POST'])
def login():
    return views.create_token()


@app.route('/authentication/users', methods=['GET', 'POST', 'PUT', 'DELETE'])
def users():
    return views.users_view()
