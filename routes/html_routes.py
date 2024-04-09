from flask import Blueprint, render_template, redirect, url_for,jsonify, flash
from models import Customer, Order, Product
from db import db

#Creates a Blueprint for HTML route
url_bp = Blueprint('html', __name__)

#Route for the home page
@url_bp.route('/home')
def home():
    return render_template('home.html')

#route to display all customers
@url_bp.route('/customers')
def display_customers():
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)

# Route to display all products
@url_bp.route('/products')
def display_products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@url_bp.route('/customers')
def list_customers():
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)

#route to display details of a specific customer
@url_bp.route('/customer/<int:customer_id>')
def customer_detail(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    orders = Order.query.filter_by(customer_id=customer_id)
    return render_template('customer_detail.html', customer=customer, orders=orders)

#route to list all orders
@url_bp.route('/orders')
def list_orders():
    orders = Order.query.all()
    return render_template('orders.html', orders=orders)

#route to display details of a specific order
@url_bp.route('/order/<int:order_id>')
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('order_detail.html', order=order)

#route to delete a order
@url_bp.route('/orders/<int:order_id>/delete', methods=['POST'])
def order_delete(order_id):
    order= Order.query.get_or_404(order_id)
    if order.processed:
        flash("Processrf orders cant be deleted")
        return redirect(url_for('html.order_detail', order_id=order_id))
    
        
    db.session.delete(order)
    db.session.commit()
    flash("order deleted", "success")
    return redirect(url_for('html.list_orders'))

#route to process a specific order
@url_bp.route('/order/<int:order_id>/process', methods=['POST'])
def process_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.processed:
        flash("This order has already been prosseced")
        return redirect(url_for('html.order_detail', order_id=order_id))
    success, message = order.process(strategy='adjust')
    flash(message, "success" if success else "error")
    return redirect(url_for('html.order_detail', order_id=order_id))