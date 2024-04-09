from flask import Blueprint, jsonify, request
from models import Order, Customer, Product, ProductOrder
from db import db
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

#create flask blueprint for ordersb
api_orders_bp = Blueprint('api_orders', __name__)

#route for creating new order
@api_orders_bp.route('/', methods=['POST'])
def create_order_api():
    try:
        data = request.get_json()
        customer_id = data.get('customer_id')
        item_data = data.get('items')
        
        #make sure customerid and items are there
        if customer_id is None or item_data is None:
            return jsonify({'error': 'missing id or items in request'}), 400
        
        
        customer = Customer.query.get_or_404(customer_id)
        #create a new order for the customer mentioned
        new_order = Order(customer=customer)
        db.session.add(new_order)

        #Iterate over all the items in the order
        for item in item_data:
            product_name = item.get('name')
            quantity = item.get('quantity')

            #Make sure product name and quantity are there
            if not product_name or quantity is None or not isinstance(quantity, int) or quantity < 1:
                db.session.rollback()
                return jsonify({'error': f"wrong product name or quantity {product_name}"}), 400
            
            #get the product by its name
            product = Product.query.filter_by(name=product_name).first()
            if not product:
                db.session.rollback() 
                return jsonify({'error': f"Product name {product_name} not found"}), 404
            
            product_order = ProductOrder(order=new_order, product=product, quantity=quantity)
            db.session.add(product_order)
        #add to the database
        db.session.commit()
        return jsonify(new_order.to_json()), 201
    #takes care of database errors
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error', 'message': str(e)}), 500

#route for processing orders
@api_orders_bp.route('/<int:order_id>', methods=['PUT'])
def api_process_order(order_id):
    data = request.get_json()
    process = data.get('process')
    strategy = data.get('strategy', 'adjust')
    
    #make sure process feild is true
    if process is not True:
        return jsonify({"error": "value must be true"}), 400
    
    #make sure strategy matches the ones that are allowed
    if strategy not in ['adjust', 'reject', 'ignore']:
        return jsonify({"error": "strategy value is invalid"}), 400
    
    #get order by id 
    order = Order.query.get_or_404(order_id)
    
    #process order with givin strat
    success, message = order.process(strategy=strategy)
    if success:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"error": message}), 400
    

