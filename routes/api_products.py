from flask import Blueprint, jsonify, request
from db import db
from models import Product

#create blueprint for products
api_products_bp = Blueprint('api_products', __name__)

#route for getting all product in json
@api_products_bp.route("/")
def products_json():
    products = Product.query.all()
    json_products = [products.to_json() for products in products] 
    return jsonify(json_products)

#route to create a new product
@api_products_bp.route("/", methods=["POST"])
def create_product():
    data = request.json
    #make sure name and price are in the request
    if 'name' not in data or 'price' not in data or not isinstance(data['price'], (int, float)) or 'available' not in data or not isinstance(data['available'], int):
        return "Invalid request", 400
    
    #create new product with givin info
    product = Product(name=data['name'], price=data['price'], available=data['available'])
    #add the product to the database
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_json()), 201

#route for updating a product
@api_products_bp.route("/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    data = request.json
    product = Product.query.get_or_404(product_id)

    #upgrade name and price with the info provided
    if 'name' in data:
        product.name = data['name']
    if 'price' in data and isinstance(data['price'], (int, float)):
        product.price = data['price']
    
    #add changes to the database
    db.session.commit()
    return "", 204

#route for deleting a product
@api_products_bp.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    #get the product for the id
    product = Product.query.get_or_404(product_id)
    #delete the product from the database
    db.session.delete(product)
    db.session.commit()
    return "", 204

#route for getting info of a product
@api_products_bp.route("/<int:product_id>")
def product_information(product_id):
    #get the product by the id
    product = Product.query.get(product_id)
    if product:
        #if the product exist return the info in json format
        return jsonify(product.to_json())
    else:
        #error if product doesnt exist
        return jsonify({"error": "Product not found"}), 404


