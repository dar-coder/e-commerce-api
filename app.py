from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime
import requests, json

from helpers import is_valid, convert_to_currency

app = Flask(__name__)

def db_connection():
    """Connect application to database"""
    
    conn = None
    try:
        conn = sqlite3.connect("database.sqlite3")
    except sqlite3.error as e:
        print(e)
    return conn

@app.route("/buyers", methods=["GET", "POST"])
def buyers():
    """Display list of all buyers (if endpoint is accessed using a "GET" request),
    and inserts a new buyer into database (if endpoint is accessed using a "POST" request)"""
    
    # Connect to database
    conn = db_connection()
    db = conn.cursor()

    # If endpoint is accessed using a "GET" request, fetch all buyers from database and add them to a list that gets returned
    if request.method == "GET":
        buyers = []
        data = db.execute("SELECT * FROM buyers").fetchall()
        
        # If there are no buyers in the database, return False
        if (data is None) or (len(data) == 0):
            return jsonify({"success": False, "message": "There are no buyers in the database"})
        
        # Each buyer is a dictionary that gets added to the list
        for row in data:
            buyer = {}
            buyer["id"] = row[0]
            buyer["first_name"] = row[1]
            buyer["last_name"] = row[2]
            buyer["email"] = row[3]
            buyer["credit_card"] = row[4]
            buyer["time_profile_created"] = row[5]
            buyer["address"] = {}
            buyer["address"]["street_name"] = row[6]
            buyer["address"]["street_number"] = row[7]
            buyer["address"]["zip_code"] = row[8]
            buyer["address"]["city"] = row[9]
            buyer["address"]["country"] = row[10]

            buyers.append(buyer)

        return jsonify({"success": True, "buyers": buyers})

    # If endpoint is accessed using a "POST" request, validate the inputs and insert the new buyer into the database
    if request.method == "POST":
        # Check if all necessary keys are in the request form
        form_keys = ["first_name", "last_name", "email", "credit_card", "address_street_name", "address_street_number", "address_zip_code", "address_city", "address_country"]
        for key in form_keys:
            if key not in request.form:
                return jsonify({"success": False, "message": f"Key '{key}' must be in request form"})

        first_name = request.form["first_name"]    
        last_name = request.form["last_name"]
        email = request.form["email"]
        credit_card = request.form["credit_card"]
        # Credit card is optional, but if provided, validate its number. If it's not valid, return False
        if not credit_card:
            credit_card = None
        else:
            is_valid_credit_card = is_valid(credit_card)
            if is_valid_credit_card == True:
                pass
            else:
                return jsonify({"success": False, "message": is_valid_credit_card[1]})
        time_profile_created = datetime.now()
        address_street_name = request.form["address_street_name"]
        address_street_number = request.form["address_street_number"]
        address_zip_code = request.form["address_zip_code"]
        address_city = request.form["address_city"]
        address_country = request.form["address_country"]

        # If a required input is not provided, return False
        if not first_name or not last_name or not email or not address_street_name or not address_street_number or not address_zip_code or not address_city or not address_country:
            return jsonify({"success": False, "message": "You must provide all necessary data"})

        # Insert the new buyer into database
        db.execute("INSERT INTO buyers ( \
            first_name, last_name, email, credit_card, profile_created, address_street_name, address_street_number, address_zip_code, address_city, address_country) VALUES ( \
                :first_name, :last_name, :email, :credit_card, :time_profile_created, :address_street_name, :address_street_number, :address_zip_code, :address_city, :address_country)", {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "credit_card": credit_card,
                    "time_profile_created": time_profile_created,
                    "address_street_name": address_street_name,
                    "address_street_number": address_street_number,
                    "address_zip_code": address_zip_code,
                    "address_city": address_city,
                    "address_country": address_country
                })
        
        conn.commit()

        return jsonify({"success": True, "message": "Buyer successfuly added to database"})


@app.route("/buyers/delete/<int:id>", methods=["DELETE"])
def delete_buyer(id):
    """Delete a buyer with a certain id"""

    # Connect to database
    conn = db_connection()
    db = conn.cursor()

    # Check the database for a buyer with the provided id. If there is no such buyer, return False, else, delete buyer from database
    buyer = db.execute("SELECT * FROM buyers WHERE id = :id", {"id": id}).fetchone()
    if buyer is None:
        return jsonify({"success": False, "message": f"No buyer with id {id} in database"})

    db.execute("DELETE FROM buyers WHERE id = :id", {"id": id})
    conn.commit()

    return jsonify({"success": True, "message": f"Buyer with id {id} successfully deleted from database"})


@app.route("/products", methods=["GET", "POST"])
def products():
    """Display list of all products sorted by price in ascending order (if endpoint is accessed using a "GET" request),
    and inserts a new product into database (if endpoint is accessed using a "POST" request)"""
    
    # Connect to database
    conn = db_connection()
    db = conn.cursor()

    # If endpoint is accessed using a "GET" request, fetch all products from database and add them to a list that gets returned
    if request.method == "GET":
        data = db.execute("SELECT * FROM products ORDER BY id ASC").fetchall()
        
        # If there are no products in database, return False
        if data == None or len(data) == 0:
            return jsonify({"success": False, "message": "There are no products in the database"})

        products = []

        # Each product is a dictionary that gets added to the list
        for row in data:
            product = {}
            product["id"] = row[0]
            product["name"] = row[1]
            product["category"] = row[2]
            product["quantity"] = row[3]
            product["size"] = row[4]
            product["price"] = row[5]
            product["currency"] = row[6]

            products.append(product)

        return jsonify({"success": True, "products": products})

    # If endpoint is accessed using a "POST" request, validate the inputs and insert the new product into the database
    if request.method == "POST":
        # Check if all necessary keys are in the request form
        form_keys = ["name", "category", "quantity", "size", "price", "currency"]
        for key in form_keys:
            if key not in request.form:
                return jsonify({"success": False, "message": f"Key '{key}' must be in request form"})

        name = request.form["name"]
        category = request.form["category"]
        
        # Check if provided quantity and price are numeric. If not, treat them as not provided
        try:
            quantity = int(request.form["quantity"])
        except:
            quantity = None
        
        try:
            price = float(request.form["price"])
        except:
            price = None

        size = request.form["size"]
        currency = request.form["currency"]

        # If a required input is not provided, return False
        if not name or not category or not quantity or not size or not price or not currency:
            return jsonify({"success": False, "message": "You must provide all necessary data"})

        # Check if the provided product category is allowed. If not allowed, return False
        categories = ["TRENERKI", "PIZAMI", "BLUZI"]
        if category.upper() not in categories:
            return jsonify({"success": False, "message": "Product category must be one of the following: Trenerki, pizami, bluzi"})

        # Check if the provided product size is allowed. If not allowed, return False
        sizes = ["S", "M", "L", "XL"]
        if size.upper() not in sizes:
            return jsonify({"success": False, "message": "Product size must be one of the following: S, M, L, XL"})

        # Check if the provided currency is allowed. If not, return False
        currencies = ["MKD", "EUR", "USD"]
        if currency.upper() not in currencies:
            return jsonify({"success": False, "message": "Currency must be one of the following: MKD, EUR or USD"})

        # Insert the new product into the database
        db.execute("INSERT INTO products (product_name, product_category, quantity, size, price, currency) VALUES (\
            :name, :category, :quantity, :size, :price, :currency)", {
                "name": name,
                "category": category,
                "quantity": quantity,
                "size": size.upper(),
                "price": price,
                "currency": currency.upper()
            })
        conn.commit()

        return jsonify({"success": True, "message": "Product successfully added to database"})


@app.route("/products/<desired_currency>", methods=["GET"])
def convert_price(desired_currency):
    """Converts the price of all products into desired (provided) currency 
    and displays a list of all products sorted by price in ascending order"""
    
    # Connect to database
    conn = db_connection()
    db = conn.cursor()

    desired_currency = desired_currency.upper()
    
    # Check if desired currency is allowed. If not, return False
    currencies = ["MKD", "EUR", "USD"]
    if desired_currency.upper() not in currencies:
        return jsonify({"success": False, "message": "Currency must be one of the following: MKD, EUR or USD"})
    
    # Check database for products. If there are no products, return False
    data = db.execute("SELECT * FROM products").fetchall()
    if data is None or len(data) == 0:
        return jsonify({"success": False, "message": "There are no products in the database"})

    # Create an empty list that will contain all products
    products = []

    # Each product is a dictionary that gets added to the list
    for row in data:
        product = {}
        product["id"] = row[0]
        product["name"] = row[1]
        product["category"] = row[2]
        product["quantity"] = row[3]
        product["size"] = row[4]
        price = row[5]
        original_currency = row[6]
        # If the currency of the product in the database is different from the desired currency, convert the price into the desired currency
        if original_currency != desired_currency:
            price = convert_to_currency(original_currency, desired_currency, price)
        product["price"] = price
        # The product will be displayed with the desired currency
        product["currency"] = desired_currency

        products.append(product)

    # Sort the list of products by product price (from lowest to highest)
    products = sorted(products, key=lambda d: d["price"])

    return jsonify({"success": True, "products": products})



@app.route("/products/delete/<int:id>", methods=["DELETE"])
def delete_product(id):
    """Delete a product with certain id"""
    
    # Connect to database
    conn = db_connection()
    db = conn.cursor()

    # Check the database for product with provided id. If there is no such product, return False
    product = db.execute("SELECT * FROM products WHERE id = :id", {"id": id}).fetchone()
    if product is None:
        return jsonify({"success": False, "message": f"No product with id {id} in database"})

    # Delete the product from the database
    db.execute("DELETE FROM products WHERE id = :id", {"id": id})
    conn.commit()

    return jsonify({"success": True, "message": f"Product with id {id} successfully deleted from database"})


if __name__=="__main__":
    app.run(debug=True)