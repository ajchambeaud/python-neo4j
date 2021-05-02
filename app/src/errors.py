from werkzeug.exceptions import HTTPException

class ProductNotFound(HTTPException):
    def __init__(self, productId):
        self.code = 404
        self.type = "ProductNotFound"
        self.description = f"Product {productId} not found."

class UserNotFound(HTTPException):
    def __init__(self, userId):
        self.code = 404
        self.type = "UserNotFound"
        self.description = f"User {userId} not found."

class PurchaseNotFound(HTTPException):
    def __init__(self, purchaseId):
        self.code = 404
        self.type = "PurchaseNotFound"
        self.description = f"Purchase {purchaseId} not found."

class MissingParameter(HTTPException):
    def __init__(self, parameter):
        self.code = 400
        self.type = "MissingParameter"
        self.description = f"Parameter '{parameter}' is required."