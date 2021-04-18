from flask import (Blueprint, request, jsonify)
from uuid import uuid1
from . import model
from flask import current_app

bp = Blueprint('user', __name__, url_prefix='/users')

@bp.route('/')
def get_users():
    try:
        return jsonify(model.get_all()), 200
    except Exception as e:
        current_app.logger.error(e)
        return { 'message': 'Internal server error' }, 500


@bp.route('/<id>')
def get_user(id):
    try:
        user = model.get(id)
        if (user == None):
            return {'message':'User not found'}, 404
        return user, 200

    except Exception as e:
        current_app.logger.error(e)
        return { 'message': 'Internal server error' }, 500


@bp.route('/', methods=['POST'])
def post_user():
    try:
        user = request.get_json()
        saved = model.save(user)
        return jsonify(saved), 201

    except Exception as e:
        current_app.logger.error(e)
        return { 'message': 'Internal server error' }, 500


@bp.route('/', methods=['PUT'])
def update_user():
    try:
        user = request.get_json()
        if (not 'id' in user):
            return {'message':'Missing user id'}, 400

        updated = model.update(user)
        if (updated == None):
            return {'message':'User not found'}, 404

        return updated, 200

    except Exception as e:
        current_app.logger.error(e)
        return { 'message': 'Internal server error' }, 500


@bp.route('/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        deleted = model.delete(id)
        if (deleted == None):
            return {'message':'User not found'}, 404
        return deleted, 200

    except Exception as e:
        current_app.logger.error(e)
        return { 'message': 'Internal server error' }, 500
