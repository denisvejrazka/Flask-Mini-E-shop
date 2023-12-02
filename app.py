from flask import Flask, render_template, request
import pymongo

app = Flask(__name__)
client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
shop = client["shop"]
customers = shop["customers"]
products = shop["products"]

def insert_docs():
    myapples = [
        {'_id': 1, 'name': 'red-apple', 'price': 2.99, 'info': 'Sweet, red apple', 'category': 'fruit', 'display_name': 'Red Apple', 'quantity': 100},
        {'_id': 2, 'name': 'green-apple', 'price': 2.99, 'info': 'Sour, green apple', 'category': 'fruit', 'display_name': 'Green Apple', 'quantity': 100},
    ]
    apples = products.insert_many(myapples)

@app.route("/")
def index():
    fruit = products.find()
    return render_template('index.html', fruit=fruit)

@app.route("/fruit")
def fruit():
    return render_template("fruit.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)