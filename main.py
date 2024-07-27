from flask import Flask, render_template, request,jsonify, flash, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '0717'
app.config['MYSQL_DB'] = 'cs115'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize MySQL
mysql = MySQL(app)

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    userid = request.form.get('userid')
    password = request.form.get('password')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM stafflogin WHERE username=%s AND password=%s", (userid, password))
    data = cur.fetchall()
    cur.close()

    if len(data) > 0:
        return render_template('home.html')
    else:
        return 'User Not Found'

@app.route('/add_item', methods=['POST'])
def add_item():
    name = request.form.get('ItemName')
    amount = request.form.get('Amount')
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO items (item_name, amount) VALUES (%s, %s)", (name, amount))
    mysql.connection.commit()
    cur.close()
    return redirect('/home')

@app.route('/add_customer', methods=['POST'])
def add_customer():
    name = request.form.get('name')
    number = request.form.get('number')
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO customers (name, contact_number) VALUES (%s, %s)", (name, number))
    mysql.connection.commit()
    cur.close()
    return redirect('/home')

@app.route('/add_order', methods=['POST'])
def add_order():
    item_id = request.form.get('item_id').split(',')
    quantity = list(map(int, request.form.get('quantity').split(',')))
    table = int(request.form.get('table_no'))
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO orders (table_no) VALUES (%s)', (table,))
    mysql.connection.commit()
    cur.execute('SELECT * FROM orders ORDER BY order_id DESC LIMIT 1')
    order_id = cur.fetchall()[0]['order_id']
    for i in range(len(item_id)):
        cur.execute('INSERT INTO order_item VALUES (%s, %s, %s)', (order_id, item_id[i], quantity[i]))
    mysql.connection.commit()
    cur.close()
    return redirect('/home')

@app.route('/delete/menu/<int:id>', methods=['POST'])
def delete_menu(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM items WHERE item_id = %s', (id,))
        mysql.connection.commit()
        cur.close()
        return redirect('/home/menu')
    except mysql.connection.Error as err:
        return jsonify({'message': 'Error deleting Item: {}'.format(err)}), 500
    
#     @app.route('/delete/donor/<int:id>', methods=['POST'])
# def delete_donor(id):
#     try:
#         cur = mysql.connection.cursor()
#         cur.execute('DELETE FROM donor_r WHERE donor_id = %s', (id,))
#         mysql.connection.commit()
#         cur.close()
#         return redirect('/home/donors')
#     except mysql.connection.Error as err:
#         return jsonify({'message': 'Error deleting donor: {}'.format(err)}), 500
    
#     @app.route('/delete/donor/<int:id>', methods=['POST'])
# def delete_donor(id):
#     try:
#         cur = mysql.connection.cursor()
#         cur.execute('DELETE FROM donor_r WHERE donor_id = %s', (id,))
#         mysql.connection.commit()
#         cur.close()
#         return redirect('/home/donors')
#     except mysql.connection.Error as err:
#         return jsonify({'message': 'Error deleting donor: {}'.format(err)}), 500

@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/home/order')
def order_page():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM orders")
    data = cur.fetchall()
    cur.close()
    return render_template('order.html', orders=data)

@app.route('/home/customer')
def customer_page():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM customers")
    data = cur.fetchall()
    cur.close()
    return render_template('customer.html', customers=data)

@app.route('/home/menu')
def menu_page():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM items")
    data = cur.fetchall()
    cur.close()
    return render_template('menu.html', items=data)

@app.route('/home/item_entry')
def item_entry_page():
    return render_template('item_entry.html')

@app.route('/home/customer_entry')
def customer_entry_page():
    return render_template('customer_entry.html')

@app.route('/home/order_item')
def order_items_page():
    return render_template('order_item.html')

if __name__ == '__main__':
    app.run(debug=True,port=5000)