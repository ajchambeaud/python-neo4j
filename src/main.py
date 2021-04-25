from flask import Flask
from users import routes as userRoutes
from products import routes as productRoutes

app = Flask(__name__)
app.url_map.strict_slashes = False

app.register_blueprint(userRoutes.bp)
app.register_blueprint(productRoutes.bp)

@app.route('/')
def hello_world():
    return {
        "message": "Chiao World"
    }
