from flask import Flask, request, jsonify , render_template, redirect
from sql_connection import get_sql_connection
import mysql.connector
import json

import products_dao
import orders_dao
import uom_dao

app = Flask(__name__, static_folder="static", static_url_path='', template_folder='templates')

connection = get_sql_connection()

@app.route('/getUOM', methods=['GET'])
def get_uom():
    response = uom_dao.get_uoms(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getProducts', methods=['GET'])
def get_products():
    response = products_dao.get_all_products(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getAllProducts', methods=['GET'])
def get_All_products():
    response = products_dao.get_all_products(connection)
    return render_template('manage_product.html', res=response)

@app.route('/insertProduct', methods=['POST'])
def insert_product():
    request_payload = request.form
    product_id = products_dao.insert_new_product(connection, request_payload)
    # response = jsonify({
    #     'product_id': product_id
    # })
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return redirect('/getAllProducts')

@app.route('/', methods=['GET'])
def get_all_orders():
    response = orders_dao.get_all_orders(connection)
    return render_template("index.html", response=response)

@app.route('/insertOrder', methods=['GET', 'POST'])
def insert_order():
    if request.method=='POST':
        request_payload = json.loads(request.form['data'])
        order_id = orders_dao.insert_order(connection, request_payload)
        # response = jsonify({
        #     'order_id': order_id
        # })
        # response.headers.add('Access-Control-Allow-Origin', '*')
        return redirect('/')
    return render_template('order.html')

@app.route('/deleteOrder/<id>', methods=['GET'])
def delete_order(id):
    details=orders_dao.get_order_details(connection, id)
    print(details)
    return render_template('delete_order.html', d=details)

@app.route('/removeOrder', methods=['POST'])
def remove_order():
    return_id = orders_dao.remove_order(connection, int(request.form['order_id']))
    # response = jsonify({
    #     'product_id': return_id
    # })
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return redirect('/')


@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    return_id = products_dao.delete_product(connection, int(request.form['product_id']))
    # response = jsonify({
    #     'product_id': return_id
    # })
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return redirect('/getAllProducts')

@app.route('/updateProduct', methods=['POST'])
def update_product():
    request_payload = request.form
    product_id = products_dao.edit_product(connection, request_payload)
    return redirect('/getAllProducts') 


@app.route('/editProduct/<id>', methods=['GET'])
def edit_product(id):
    details=products_dao.get_product_details(connection, id)
    print(details)
    return render_template('product_details.html', d=details)

if __name__ == "__main__":
    print("Starting Python Flask Server For Grocery Store Management System")
    app.run(debug=True)

