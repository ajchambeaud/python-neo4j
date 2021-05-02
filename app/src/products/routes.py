from flask import (Blueprint, request, jsonify)
from flask import current_app
from errors import ProductNotFound, MissingParameter
from . import model

bp = Blueprint('product', __name__, url_prefix='/products')

@bp.route('/')
def get_products():
    author = request.args.get('author')
    category = request.args.get('category')

    return jsonify(model.get_all(author, category)), 200


@bp.route('/<id>')
def get_product(id):
    product = model.get(id)

    if (product == None):
        raise ProductNotFound(id)

    return product, 200


@bp.route('/', methods=['POST'])
def create_product():
    product = request.get_json()
    saved = model.save(product)

    return jsonify(saved), 201


@bp.route('/', methods=['PUT'])
def update_product():
    product = request.get_json()

    if (not 'id' in product):
        raise MissingParameter('id')

    updated = model.update(product)

    if (updated == None):
        raise ProductNotFound(product['id'])

    return updated, 200


@bp.route('/<id>', methods=['DELETE'])
def delete_product(id):
    deleted = model.delete(id)

    if (deleted == None):
        raise ProductNotFound(deleted['id'])

    return deleted, 200