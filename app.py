from flask import Flask, render_template, request, redirect, url_for
import pymongo

app = Flask(__name__)
client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
shop = client["shop"]
customers = shop["customers"]
products = shop["products"]
#orders = shop["orders"]

cart = []
products.update_one({"display_name": "Pear"}, {"$set": {"quantity": 70}})
quantities = []
def get_quantites():
    for product in products.find():
        quantities.append(product["quantity"])
    return quantities
get_quantites()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/fruit")
def fruit():
    fruit = products.find({"category": "fruit"})
    return render_template("fruit.html", fruit=fruit)

@app.route("/add_fruit_to_cart", methods=['POST'])
def add_fruit_to_cart():
    selected_fruit_id = request.form.get('product-btn')
    desired_fruit = products.find_one({"_id": int(selected_fruit_id)})
    if desired_fruit and desired_fruit['quantity'] > 0:
        products.update_one({"_id": int(selected_fruit_id)}, {"$inc": {"quantity": -1}})
        cart.append(desired_fruit)
    return redirect(url_for('fruit'))

@app.route("/cart")
def shopping_cart():
    for product_id in cart:
        product = products.find({"_id": product_id})
        
    return render_template("cart.html", cart=cart)

@app.route("/vegetables")
def vegetables():
    vegetables = products.find({"category": "vegetable"})
    return render_template("vegetables.html", vegetables=vegetables)

@app.route("/add_vege_to_cart", methods=['POST'])
def add_vege_to_cart():
    selected_vege_id = request.form.get('product-btn')
    desired_vege = products.find_one({"_id": int(selected_vege_id)})
    if desired_vege and desired_vege['quantity'] > 1:
        products.update_one({"_id": int(selected_vege_id)}, {"$inc": {"quantity": -1}})
        cart.append(desired_vege)
    return redirect(url_for('vegetables'))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)