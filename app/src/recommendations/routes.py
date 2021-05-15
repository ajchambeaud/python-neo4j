from flask import (Blueprint, request, jsonify)
from . import model
from flask import current_app
from errors import UserNotFound, MissingParameter

bp = Blueprint('recommendations', __name__, url_prefix='/recommendations')

@bp.route('/bycategory/<category>')
def by_category(category):
    """
    Category best sellers.
    """
    return jsonify(model.get_best_sellers(category)), 200


@bp.route('/relatedproducts/<id>')
def get_user(id):
    """
    Customers also bought these products.
    """
    return jsonify(model.get_customers_also_bought(id)), 200
