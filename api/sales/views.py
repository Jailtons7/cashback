from flask import request, jsonify, g
from mongoengine.errors import ValidationError, NotUniqueError

from api.sales.models import Purchase
from config.settings import Settings
from integrations.boticario import BoticarioCashback


def purchase_view():
    if request.method == 'POST':
        data = request.json

        try:
            purchase = Purchase(**data)
            purchase.set_user(g.user)
            purchase.save()
            return jsonify({
                'msg': 'Successfully added',
                'data': purchase
            }), 201
        except TypeError as e:
            print(e)
            return jsonify({'msg': Purchase.required_fields()}), 400
        except ValidationError as e:
            print(e.message)
            return jsonify({'msg': e.message}), 400
        except NotUniqueError as e:
            return jsonify({'msg': f"There's already a purchase with code '{data['code']}'"}), 400

    elif request.method == 'GET':
        try:
            page = int(request.args.get('page', 1))
        except ValueError:
            # If user set an invalid value in page parameter, page will be the first
            page = 1

        per_page = Settings.PAGINATION

        purchases = Purchase.objects(user=g.user).paginate(page=page, per_page=per_page)
        tot = Purchase.objects.count()
        return jsonify({
            'total': tot,
            'msg': 'Successfully fetched',
            'data': [purchase for purchase in purchases.items]
        }), 200


def cashback_view(cpf):
    monthly_cashback = Purchase.get_monthly_cashback(cpf=cpf)
    credit = BoticarioCashback.get_boticario_credits(cpf=cpf)
    if credit is not None:
        return jsonify({
            "msg": "Successfully fetched",
            "cashback": monthly_cashback + credit
        }), 200
    return jsonify({
        "msg": "Service unavailable. Please try again later"
    }), 503
