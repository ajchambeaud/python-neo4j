from flask import (Blueprint, request, jsonify)
from uuid import uuid1
from . import model
from flask import current_app
from users import model as userModel

bp = Blueprint('purchase', __name__, url_prefix='/purchases')

@bp.route('/<user_id>')
def get_purchases(user_id):
    try:
        return jsonify(model.get_all(user_id)), 200
    except Exception as e:
        current_app.logger.error(e)
        return { 'message': 'Internal server error' }, 500


@bp.route('/<user_id>/<id>')
def get_purchase(user_id, id):
    try:
        user = userModel.get(user_id)

        if (user is None):
            return {'message':'User not found'}, 404

        purchase = model.get(user_id, id)

        if (purchase == None):
            return {'message':'Purchase not found'}, 404

        return purchase, 200

    except Exception as e:
        current_app.logger.error(e)
        return { 'message': 'Internal server error' }, 500


@bp.route('/<user_id>', methods=['POST'])
def post_purchase(user_id):
    try:
        user = userModel.get(user_id)

        if (user is None):
            return {'message':'User not found'}, 404

        items = request.get_json()
        purchase = model.save(user, items)
        return jsonify(purchase), 201

    except model.ProductNotFound as e:
        current_app.logger.error(e)
        return { 'message': f"Product {e.productId} not found" }, 404

    except Exception as e:
        current_app.logger.error(e)
        return { 'message': 'Internal server error' }, 500

