from flask_jwt_extended import jwt_required

from api import app
from api.sales import views


@app.route('/purchases', methods=["GET", "POST"], strict_slashes=False)
@jwt_required()
def purchases():
    return views.purchase_view()
