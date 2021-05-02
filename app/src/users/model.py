from uuid import uuid1
from database.neo import NeoDB
import sys
from flask import current_app

def recod_to_user (record):
    return {
        'id': record['id'], 
        'name': record['name'], 
        'lastName': record['lastName'], 
        'email': record['email']
    } 


def get_all():
    session = NeoDB().getSession()

    query = """
        MATCH (n:User) 
        RETURN 
            n.id as id, 
            n.name as name, 
            n.lastName as lastName, 
            n.email as email
    """

    data = session.run(query).data()

    session.close()
    return data


def get(id):
    session = NeoDB().getSession()

    query = """
        MATCH (n:User {id: $id})
        RETURN 
            n.id as id, 
            n.name as name, 
            n.lastName as lastName, 
            n.email as email
    """

    result = session.run(query, id=id).single()
    data = result.data() if result != None else result

    session.close()
    return data


def save(user):
    user['id'] = str(uuid1())
    session = NeoDB().getSession()

    query = """
        CREATE (n:User { 
            id: $id,
            name: $name, 
            lastName: $lastName, 
            email: $email
        }) RETURN 
            n.id as id, 
            n.name as name, 
            n.lastName as lastName, 
            n.email as email
    """

    result = session.write_transaction(lambda tx: tx.run(query,user).single()) 
    data = result.data() if result != None else result

    session.close()
    return data


def delete(id):
    session = NeoDB().getSession()

    query = """
    MATCH (n:User {id: $id})
    WITH n,
         n.id as id, 
         n.name as name, 
         n.lastName as lastName, 
         n.email as email
    DETACH DELETE n
    RETURN id, name, lastName, email
    """

    result = session.write_transaction(lambda tx: tx.run(query,id=id).single()) 
    data = result.data() if result != None else result

    session.close()
    return data

def update(updated):
    session = NeoDB().getSession()

    query = """
    MATCH (n:User {id: $id})
    SET n.name = $name, 
        n.lastName = $lastName, 
        n.email = $email
    RETURN
        n.id as id, 
        n.name as name, 
        n.lastName as lastName, 
        n.email as email
    """

    result = session.write_transaction(lambda tx: tx.run(query,updated).single()) 
    data = result.data() if result != None else result

    session.close()
    return data
