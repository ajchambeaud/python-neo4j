from uuid import uuid1

database = { "users": [] }

def get_all():
    return database["users"]

def get(id):
    user = next((item for item in database["users"] if item["id"] == id), None)
    return user

def save(user):
    user["id"] = str(uuid1())
    database["users"].append(user)
    return user

def delete(id):
    deleted = next((user for user in database["users"] if user["id"] == id), None)
    database["users"] = [user for user in database["users"] if user["id"] != id]
    return deleted

def update(updated):
    database["users"] = [user if user["id"] != updated["id"] else updated for user in database["users"]]
    return next((user for user in database["users"] if user["id"] == updated["id"]), None)
