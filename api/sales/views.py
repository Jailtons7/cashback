from flask import request, jsonify
from mongoengine.errors import ValidationError, NotUniqueError

from api.sales.models import Purchase
from config.settings import Settings


def purchase_view():
    if request.method == 'POST':
        data = request.json

        try:
            purchase = Purchase(**data)
        except TypeError as e:
            print(e)
            return jsonify({'msg': Purchase.required_fields()}), 400

        try:
            purchase.save()
            return jsonify({
                'msg': 'Successfully added',
                'data': purchase
            })
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

        purchases = Purchase.objects.paginate(page=page, per_page=per_page)
        tot = Purchase.objects.count()
        return jsonify({
            'total': tot,
            'msg': 'Successfully fetched',
            'data': [purchase for purchase in purchases.items]
        }), 200
