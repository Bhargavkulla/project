from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",  # Change as needed
    database="ecommerce_db"
)
cursor = db.cursor()

def create_tables():
    cursor.execute("CREATE TABLE IF NOT EXISTS shoes (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), price FLOAT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS watches (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), price FLOAT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS paintings (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), price FLOAT)")

create_tables()

@app.route('/add/<item>', methods=['POST'])
def add_item(item):
    data = request.json
    name = data.get('name')
    price = data.get('price')
    cursor.execute(f"INSERT INTO {item} (name, price) VALUES (%s, %s)", (name, price))
    db.commit()
    return jsonify({"message": f"{item} added"}), 201

@app.route('/get/<item>', methods=['GET'])
def get_items(item):
    cursor.execute(f"SELECT * FROM {item}")
    result = cursor.fetchall()
    return jsonify(result)

@app.route('/delete/<item>/<int:item_id>', methods=['DELETE'])
def delete_item(item, item_id):
    cursor.execute(f"DELETE FROM {item} WHERE id = %s", (item_id,))
    db.commit()
    return jsonify({"message": f"{item} deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
