from uuid import uuid1
from flask import current_app
from database.neo import NeoDB

def save(user, products):
    session = NeoDB().getSession()

    id_purchase = str(uuid1())

    query = f"MATCH (u:User {{id: '{user['id']}'}}) "
    
    for product in products:
        pid = product['id'].replace('-', '')
        query += f",(p{pid}:Product {{id: '{product['id']}'}})"

    query += " CREATE "

    for product in products:
        pid = product['id'].replace('-', '')
        query += f"""
        (u)-[r{pid}:BOUGHT {{
            id: '{id_purchase}',
            item: '{product['title']}',
            price: {product['price']},
            quantity: {product['quantity']},
            date: timestamp()
        }}]->(p{pid}),"""

    query = query[:len(query) - 1]

    r = session.write_transaction(lambda tx: tx.run(query).data()) 

    current_app.logger.info({'result': r})

    session.close()

    return get(user['id'], id_purchase)

def get_all(user_id):
    session = NeoDB().getSession()

    query = """
        MATCH (u:User {id:$user_id})-[r:BOUGHT]->()
        WITH 
            r.id as purchaseId,
            r.date as date,
            u.id as userId,
            [item in collect(r) | item{.item, .price, .quantity}] as items
        return {
            userId: userId,
            purchaseId: purchaseId, 
            date: date, 
            items: items, 
            total: round(reduce(t=0, item in items | t + (item.price * item.quantity)), 2)
        } as purchase
    """

    result = session.run(query, user_id=user_id)

    data = [item['purchase'] for item in result.data()] if result != None else result

    session.close()
    return data


def get(user_id, id):
    session = NeoDB().getSession()

    query = """
        MATCH (u:User {id:$user_id})-[r:BOUGHT {id:$id}]->()
        WITH 
            r.id as purchaseId,
            r.date as date,
            u.id as userId,
            [item in collect(r) | item{.item, .price, .quantity}] as items
        return {
            userId: userId,
            purchaseId: purchaseId, 
            date: date, 
            items: items, 
            total: round(reduce(t=0, item in items | t + (item.price * item.quantity)), 2)
        } as purchase
    """

    result = session.run(query, user_id=user_id, id=id).single()

    data = result.data()['purchase'] if result != None else result

    session.close()
    return data