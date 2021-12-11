from sql_connection import get_sql_connection

def get_all_products(connection):
    cursor = connection.cursor()
    query = ("select products.product_id, products.name, products.uom_id, products.price_per_unit, uom.uom_name from products inner join uom on products.uom_id=uom.uom_id")
    cursor.execute(query)
    response = []
    for (product_id, name, uom_id, price_per_unit, uom_name) in cursor:
        response.append({
            'product_id': product_id,
            'name': name,
            'uom_id': uom_id,
            'price_per_unit': price_per_unit,
            'uom_name': uom_name
        })
    return response


def insert_new_product(connection, product):
    cursor = connection.cursor()
    query = ("INSERT INTO products "
             "(name, uom_id, price_per_unit)"
             "VALUES (%s, %s, %s)")
    data = (product['name'], product['uoms'], product['price'])

    cursor.execute(query, data)
    connection.commit()

    return cursor.lastrowid

def delete_product(connection, product_id):
    cursor = connection.cursor()
    query = ("DELETE FROM products where product_id=" + str(product_id))
    cursor.execute(query)
    connection.commit()
    print(cursor.lastrowid)
    return cursor.lastrowid

def edit_product(connection, product):
    cursor = connection.cursor()
    query = ("UPDATE products SET price_per_unit = (%s) WHERE product_id = (%s) " )
    data= (product['price_per_unit'], product['product_id'])
    cursor.execute(query, data)
    connection.commit()
    
    return cursor.lastrowid

def get_product_details(connection, pid):
    cursor = connection.cursor()
    query = "select products.product_id, products.name, products.uom_id, products.price_per_unit, uom.uom_name from products, uom where products.product_id= (%s) and products.uom_id=uom.uom_id"
    cursor.execute(query, (int(pid),))
    response = cursor.fetchone()
    # print(response[0])
    return response

if __name__ == '__main__':
    connection = get_sql_connection()
    # print(get_all_products(connection))
    print(edit_product(connection, {
        'product_id': 1,
        'price_per_unit': 50
    }))