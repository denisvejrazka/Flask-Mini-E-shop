from flask import Flask, render_template, request, redirect, url_for, session
import pymongo
import math
app = Flask(__name__)
app.secret_key = "secret_key1"
client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
shop = client["shop"]
products = shop["products"]
#orders = shop["orders"]

cart = []

#products.update_one({"display_name": "Pear"}, {"$set": {"quantity": 70}})
quantities = []
def get_quantites():
    for product in products.find():
        quantities.append(product["quantity"])
    return quantities
get_quantites()

for product in cart:
    print(product)

@app.route("/", methods=["GET", "POST"])
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
    global total_sum
    for product_id in cart:
        id = products.find({"_id": product_id}) 
    total_sum = calculate_total_price(cart)
    return render_template("cart.html", cart=cart, total_sum="%.2f" % total_sum)

def calculate_total_price(cart):
    total_price = 0
    for product in cart:
        total_price += product["price"]
    return total_price

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

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/cart", methods=["GET", "POST"])
def remove_from_cart():
    global total_sum
    selected_product = request.form.get("remove_from_cart_id")
    for product in cart:
        if product["_id"] == int(selected_product):
            cart.remove(product)
            print(f"Product {selected_product} removed from cart")
            desired_prod = products.find_one({"_id": int(selected_product)})
            total_sum = total_sum-desired_prod["price"]
            products.update_one({"_id": int(selected_product)}, {"$inc": {"quantity": +1}})
            break  # Stop the loop once the product is removed

    return render_template("cart.html", cart=cart, total_sum=total_sum)

@app.route("/form.html")
def form():
    global total_sum
    for product_id in cart:
        id = products.find({"_id": product_id}) 
    total_sum = calculate_total_price(cart)
    return render_template("form.html", cart=cart, total_sum="%.2f" % total_sum)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)