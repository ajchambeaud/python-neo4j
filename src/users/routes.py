from flask import (Blueprint, request, jsonify)
from uuid import uuid1
from . import model

bp = Blueprint('user', __name__, url_prefix='/users')

@bp.route('/')
def get_users():
    return jsonify(model.get_all()), 200

@bp.route('/<id>')
def get_user(id):
    user = model.get(id)
    if (user == None):
        return {'message':'User not found'}, 404
    return user, 200

@bp.route('/', methods=['POST'])
def post_user():
    user = request.get_json()
    saved = model.save(user)
    return saved, 201

@bp.route('/', methods=['PUT'])
def update_user():
    user = request.get_json()
    if (not 'id' in user):
        return {'message':'Missing user id'}, 400

    updated = model.update(user)
    if (updated == None):
        return {'message':'User not found'}, 404

    return updated, 200

@bp.route('/<id>', methods=['DELETE'])
def delete_user(id):
    deleted = model.delete(id)
    if (deleted == None):
        return {'message':'User not found'}, 404
    return deleted, 200
