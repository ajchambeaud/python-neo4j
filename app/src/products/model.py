from uuid import uuid1
from database.neo import NeoDB
from flask import current_app
import json

def recod_to_product (record):
    return {
        'id': record['id'], 
        'title': record['title'], 
        'author': record['author'],
        'category': record['category'], 
        'price': record['price']
    }


def build_filter (author, category):
    filter = []

    if (author != None):
        filter.append("author:$author")

    if (category != None):
        filter.append("category:$category")

    return "{" + ",".join(filter) + "}"


def get_all(author, category):
    session = NeoDB().getSession()

    filter = build_filter(author, category)

    query = """
        MATCH (n:Product {})
        RETURN 
            n.id as id, 
            n.title as title,
            n.author as author,
            n.category as category, 
            n.price as price
    """.format(filter)

    current_app.logger.info({query: query})

    data = session.run(query, {
        'author':author, 
        'category':category
    }).data()

    session.close()
    return data


def get(id):
    session = NeoDB().getSession()

    query = """
        MATCH (n:Product {id: $id})
        RETURN 
            n.id as id, 
            n.title as title, 
            n.author as author,
            n.category as category, 
            n.price as price
    """

    result = session.run(query, id=id).single()
    data = result.data() if result != None else result

    session.close()
    return data


def save(product):
    product['id'] = str(uuid1())
    session = NeoDB().getSession()

    query = """
        CREATE (n:Product { 
            id: $id,
            title: $title, 
            author: $author,
            category: $category, 
            price: $price
        }) RETURN
            n.id as id, 
            n.title as title, 
            n.author as author,
            n.category as category, 
            n.price as price
    """

    result = session.write_transaction(lambda tx: tx.run(query,product).single()) 
    data = result.data() if result != None else result

    session.close()
    return data


def delete(id):
    session = NeoDB().getSession()

    query = """
    MATCH (n:Product {id: $id})
    WITH n,
         n.id as id, 
         n.title as title, 
         n.author as author,
         n.category as category, 
         n.price as price
    DETACH DELETE n
    RETURN id, title, category, price
    """

    result = session.write_transaction(lambda tx: tx.run(query,id=id).single()) 
    data = result.data() if result != None else result

    session.close()
    return data


def update(updated):
    session = NeoDB().getSession()

    query = """
    MATCH (n:Product {id: $id})
    SET n.title = $title, 
        n.author = $author,
        n.category = $category, 
        n.price = $price
    RETURN
        n.id as id, 
        n.title as title,
        n.author as author,
        n.category as category,
        n.price as price
    """

    result = session.write_transaction(lambda tx: tx.run(query,updated).single()) 
    data = result.data() if result != None else result

    session.close()
    return data
