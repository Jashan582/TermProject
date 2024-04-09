from flask import Blueprint, jsonify, request
from db import db
from models import Customer

#creates blueprint for customers
api_customers_bp = Blueprint('api_customers', __name__)

#Get all customer info, returns a json list
@api_customers_bp.route("/")
def customers_json():
    customers = Customer.query.all()
    json_customers = [customer.to_json() for customer in customers]
    return jsonify(json_customers)

#This route is for updating customer info
@api_customers_bp.route("/<int:customer_id>", methods=["PUT"])
def update_customers(customer_id):
    data = request.json
    customer= Customer.query.get_or_404(customer_id)
    
    #make sure balance is in the request and is a number
    if 'balance' not in data or not isinstance(data['balance'], (int,float)):
        return "invalid request: balance", 400
    customer.balance = data['balance']
    db.session.commit()
    return "", 204

#This route allows us to create new customers
@api_customers_bp.route("/", methods=["POST"])
def create_customer():
    data = request.json
    if 'name' not in data or 'phone' not in data:
        return "Invalid request", 400
    
    #create new customer object
    customer = Customer(name=data['name'], phone=data['phone'])
    #add the new customer to the database
    db.session.add(customer)
    db.session.commit()
    return jsonify(customer.to_json()), 201

#route for deleting a customer
@api_customers_bp.route("/<int:customer_id>", methods=["DELETE"])
def delete_customers(customer_id):
    #get customer from database
    customer = Customer.query.get_or_404(customer_id)
    #delete customer from database
    db.session.delete(customer)
    db.session.commit()
    return "", 204

#route to get customer information
@api_customers_bp.route("/<int:customer_id>")
def customer_information(customer_id):
    #get customer from the database
    customer = Customer.query.get(customer_id)
    if customer:
        #return the customer in json format
        return jsonify(customer.to_json())
    else:
        #error if customer doesnt exist
        return jsonify({"error": "Customer not found"}), 404