from flask import Flask, render_template, request
import pymongo

app = Flask(__name__)
client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
shop = client["shop"]
customers = shop["customers"]
products = shop["products"]
x = { "_id": 1, "name": "red-apple", "price": 2.99, "info": "Tasty, green apple", "category": "fruit", "display_name": "Red Apple"}

fruit= products.insert_one(x)
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/fruit")
def fruit():
    return render_template("fruit.html", fruit=x)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)