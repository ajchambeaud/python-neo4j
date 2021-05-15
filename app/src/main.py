import traceback
from flask import Flask
from werkzeug.exceptions import HTTPException
from users import routes as userRoutes
from products import routes as productRoutes
from purchases import routes as purchaseRoutes
from recommendations import routes as recommendationRoutes

app = Flask(__name__)
app.url_map.strict_slashes = False

app.register_blueprint(userRoutes.bp)
app.register_blueprint(productRoutes.bp)
app.register_blueprint(purchaseRoutes.bp)
app.register_blueprint(recommendationRoutes.bp)

@app.route('/')
def ping():
    return {
        "message": "Python-Neo4j e-commerce api",
        "routes": [
            "/users",
            "/products",
            "/purchases"
        ]
    }, 200


@app.errorhandler(Exception)
def handle_exeption(e):
    app.logger.error(e)
    traceback.print_tb(e.__traceback__)

    if isinstance(e, HTTPException):
        return {
            'type': e.name if not hasattr(e, 'type') else e.type,
            'message': e.description
        }, e.code

    return { 'message': 'Internal server error' }, 500
