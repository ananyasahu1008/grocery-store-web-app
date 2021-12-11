from datetime import datetime
from sql_connection import get_sql_connection

def insert_order(connection, order):
    cursor = connection.cursor()

    order_query = ("INSERT INTO orders "
             "(name, time)"
             "VALUES (%s, %s)")
    order_data = (order['customer_name'], datetime.now())

    cursor.execute(order_query, order_data)
    order_id = cursor.lastrowid

    order_details_query = ("INSERT INTO order_details "
                           "(order_id, product_id, quantity)"
                           "VALUES (%s, %s, %s)")

    order_details_data = []
    for order_detail_record in order['order_details']:
        order_details_data.append([
            order_id,
            int(order_detail_record['product_id']),
            float(order_detail_record['quantity']),
        ])
    cursor.executemany(order_details_query, order_details_data)

    connection.commit()

    return order_id

# def get_order_details(connection, order_id):
#     cursor = connection.cursor()

#     query = "SELECT * from order_details where order_id = %s"

#     query = "SELECT order_details.order_id, "\
#             "products.name, products.price_per_unit FROM order_details LEFT JOIN products on " \
#             "order_details.product_id = products.product_id where order_details.order_id = %s"

#     data = (order_id, )

#     cursor.execute(query, data)

#     records = []
#     for (order_id, quantity, product_name, price_per_unit) in cursor:
#         records.append({
#             'order_id': order_id,
#             'quantity': quantity,
#             'product_name': product_name,
#             'price_per_unit': price_per_unit
#         })

#     cursor.close()

#     return records
def get_order_details(connection, oid):
    cursor = connection.cursor()
    query = "select order_details.order_id, order_details.product_id, order_details.quantity from order_details where order_details.order_id=(%s)"
    cursor.execute(query, (int(oid),))
    response = cursor.fetchone()
    # print(response[0])
    return response



def get_all_orders(connection):
    cursor = connection.cursor()
    query = ("SELECT * FROM orders")
    cursor.execute(query)
    res1=cursor.fetchall()
    query=("SELECT order_details.order_id, SUM(order_details.quantity*products.price_per_unit) from order_details join products on order_details.product_id=products.product_id group by order_details.order_id")
    cursor.execute(query)
    res2=cursor.fetchall()
    prices={}
    for (id, price) in res2:
        prices[id]=price
    # print(res1)
    # print(res2)
    response=[]
    for (order_id, name, dt) in res1:
        total=0
        if order_id in prices:
            total=prices[order_id]
        if total:
            response.append({
                'order_id': order_id,
                'customer_name': name,
                'total': total,
                'datetime': str(dt),
            })

    cursor.close()

    # append order details in each order
    # for record in response:
    #     record['order_details'] = get_order_details(connection, record['order_id'])

    return response

def remove_order(connection, order_id):
    cursor = connection.cursor()
    query = ("DELETE FROM orders where order_id=" + str(order_id))
    cursor.execute(query)
    connection.commit()
    print(cursor.lastrowid)
    return cursor.lastrowid    

if __name__ == '__main__':
    connection = get_sql_connection()
    print(get_all_orders(connection))
    # print(get_order_details(connection,4))
    # print(insert_order(connection, {
    #     'customer_name': 'dhaval',
    #     'total': '500',
    #     'datetime': datetime.now(),
    #     'order_details': [
    #         {
    #             'product_id': 1,
    #             'quantity': 2,
    #             'total_price': 50
    #         },
    #         {
    #             'product_id': 3,
    #             'quantity': 1,
    #             'total_price': 30
    #         }
    #     ]
    # }))