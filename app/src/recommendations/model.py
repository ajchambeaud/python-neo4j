from uuid import uuid1
from flask import current_app
from database.neo import NeoDB

def get_best_sellers(category):
    session = NeoDB().getSession()

    query = """
        MATCH (p:Product {category: $category})
        OPTIONAL MATCH (p)-[b:BOUGHT]-(u:User)
        WITH p, count(b) as purchases
        RETURN p{.*, score: purchases} as product
        ORDER BY purchases DESC
        LIMIT 5
    """

    result = session.run(query, category=category)

    data = [item['product'] for item in result.data()] if result != None else result

    session.close()
    return data


def get_customers_also_bought(product_id):
    session = NeoDB().getSession()

    query = """
        MATCH (p:Product {id: $id})-[:BOUGHT]-(u:User)-[:BOUGHT]-(p2:Product)
        WITH p2, count(*) as score
        RETURN p2{.*, score: score} as product
        ORDER BY score DESC
        LIMIT 5
    """

    result = session.run(query, id=product_id)

    data = [item['product'] for item in result.data()] if result != None else result

    session.close()
    return data