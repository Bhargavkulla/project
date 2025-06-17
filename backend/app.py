from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL database config - update these with your credentials
db_config = {
    'host': 'localhost',
    'user': 'admin',
    'password': 'admin',
    'database': 'bhargav'
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

def get_table(category):
    if category == 'shoes':
        return 'shoes'
    elif category == 'watches':
        return 'watches'
    elif category == 'paintings':
        return 'paintings'
    else:
        return None

@app.route('/add/<category>', methods=['POST'])
def add_item(category):
    table = get_table(category)
    if not table:
        return jsonify({'error': 'Invalid category'}), 400

    data = request.get_json()
    name = data.get('name')
    price = data.get('price')

    if not name or price is None:
        return jsonify({'error': 'Name and price are required'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO {table} (name, price) VALUES (%s, %s)", (name, price))
        conn.commit()
        item_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({'id': item_id, 'name': name, 'price': price}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get/<category>', methods=['GET'])
def get_items(category):
    table = get_table(category)
    if not table:
        return jsonify({'error': 'Invalid category'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT id, name, price FROM {table}")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        data = [[row[0], row[1], float(row[2])] for row in rows]
        return jsonify(data)
    except Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete/<category>/<int:item_id>', methods=['DELETE'])
def delete_item(category, item_id):
    table = get_table(category)
    if not table:
        return jsonify({'error': 'Invalid category'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table} WHERE id = %s", (item_id,))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()

        if affected == 0:
            return jsonify({'error': 'Item not found'}), 404
        return jsonify({'status': 'deleted'}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
