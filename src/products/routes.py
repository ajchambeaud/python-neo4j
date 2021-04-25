from flask import (Blueprint, request, jsonify)
from flask import current_app
from . import model

bp = Blueprint('product', __name__, url_prefix='/products')

@bp.route('/')
def get_products():
    author = request.args.get('author')
    category = request.args.get('category')

    try:
        return jsonify(model.get_all(author, category)), 200
    except Exception as e:
        current_app.logger.error(e)
        return { 'message': 'Internal server error' }, 500


@bp.route('/<id>')
def get_product(id):
    try:
        product = model.get(id)
        if (product == None):
            return {'message':'Product not found'}, 404
        return product, 200

    except Exception as e:
        current_app.logger.error(e)
        return { 'message': 'Internal server error' }, 500


@bp.route('/', methods=['POST'])
def create_product():
    try:
        product = request.get_json()
        saved = model.save(product)
        return jsonify(saved), 201

    except Exception as e:
        current_app.logger.error(e)
        return { 'message': 'Internal server error' }, 500


@bp.route('/', methods=['PUT'])
def update_product():
    try:
        product = request.get_json()
        if (not 'id' in product):
            return {'message':'Missing product id'}, 400

        updated = model.update(product)
        if (updated == None):
            return {'message':'Product not found'}, 404

        return updated, 200

    except Exception as e:
        current_app.logger.error(e)
        return { 'message': 'Internal server error' }, 500


@bp.route('/<id>', methods=['DELETE'])
def delete_product(id):
    try:
        deleted = model.delete(id)
        if (deleted == None):
            return {'message':'Product not found'}, 404
        return deleted, 200

    except Exception as e:
        current_app.logger.error(e)
        return { 'message': 'Internal server error' }, 500