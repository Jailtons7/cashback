from flask import Blueprint
from flask_jwt_extended import jwt_required

from api.sales import views


sales_blueprint = Blueprint('sales_blueprint', __name__)


@sales_blueprint.route('/purchases', methods=["GET", "POST"], strict_slashes=False)
@jwt_required()
def purchases():
    return views.purchase_view()


@sales_blueprint.route('/cashback/<string:cpf>', methods=['GET'], strict_slashes=False)
@jwt_required()
def cashback(cpf):
    return views.cashback_view(cpf)
