from sqlalchemy import Integer, String, Numeric
from db import db
from flask import Flask, render_template
import csv
from pathlib import Path
 

app = Flask(__name__)

# Route to display a list of customers
@app.route("/customers")
def display_customers():
    customers = []
    # Opens the customers CSV file and reads each row into a list.
    with open('data/customers.csv', 'r') as file:
        name = csv.DictReader(file)
        for row in name:
            customers.append(row)
    # Renders the 'customers.html' template
    return render_template('customers.html', customers=customers)

# Route to display a list of products passing in the list of products
@app.route("/products")
def display_products():
    products = []
    # Opens the products CSV file and reads each row into a list.
    with open("data/products.csv", "r") as f:
        read = csv.DictReader(f)
        for row in read:
            products.append(row)
    # Renders the 'products.html' template passing in the list of products
    return render_template('products.html', products=products)
if __name__ == "__main__":
    app.run(debug=True)