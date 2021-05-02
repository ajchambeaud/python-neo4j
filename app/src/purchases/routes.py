from flask import (Blueprint, request, jsonify)
from uuid import uuid1
from . import model
from flask import current_app
from users import model as userModel
from products import model as productModel
from errors import UserNotFound, ProductNotFound, PurchaseNotFound

bp = Blueprint('purchase', __name__, url_prefix='/purchases')

@bp.route('/<user_id>')
def get_purchases(user_id):
    return jsonify(model.get_all(user_id)), 200


@bp.route('/<user_id>/<id>')
def get_purchase(user_id, id):
    user = userModel.get(user_id)

    if (user is None):
        raise UserNotFound(user_id)

    purchase = model.get(user_id, id)

    if (purchase == None):
        raise PurchaseNotFound(id)

    return purchase, 200


@bp.route('/<user_id>', methods=['POST'])
def post_purchase(user_id):
    user = userModel.get(user_id)
    items = request.get_json()

    if (user is None):
        raise UserNotFound(user_id)

    products = []
    for item in items:
        product = productModel.get(item['productId'])

        if (product is None):
            raise ProductNotFound(item['productId'])
        
        products.append({**product, 'quantity': item['quantity']})

    purchase = model.save(user, products)

    return jsonify(purchase), 201
