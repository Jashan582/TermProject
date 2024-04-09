from app import app
from db import db
from models import Order, Customer, Product, ProductOrder
from sqlalchemy.sql import func
import csv
import random

#Create all tables based on SQLAlchemy
def create_all_tables():
    with app.app_context():
        db.create_all()

#drop all tables 
def drop_all_tables():
    with app.app_context():
        db.drop_all()

#read the initial data from the csv and seed to the database
def get_csv():
    with app.app_context():
        #read customer data from csv and add to database
        with open('data/customers.csv', 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                random_balance = random.randint(1000, 10000)  # Assign random balance to customers
                customer = Customer(name=row['name'], phone=row['phone'], balance=random_balance)
                db.session.add(customer)
        
        #read product data from csv and add to database        
        with open('data/products.csv', 'r') as file:
            read = csv.DictReader(file)
            for row in read:
                available_quantity = random.randint(10, 100)  # Assign random quantities to products
                product = Product(name=row['name'], price=row['price'], available=available_quantity)
                db.session.add(product)
        db.session.commit()
#creates random orders 
def create_random_orders(num_orders):
    with app.app_context():
        #get all customers
        customers = Customer.query.all()
        #get all products 
        products = Product.query.all()

        for _ in range(num_orders):
            # Find a random customer
            customer = random.choice(customers)
            # Make an order for that customer
            order = Order(customer=customer)
            db.session.add(order)

            # Add a random product to the order
            product = random.choice(products)
            rand_qty = random.randint(1, product.available)
            association = ProductOrder(order=order, product=product, quantity=rand_qty)
            db.session.add(association)
            
            # Commit to the database
            db.session.commit()


if __name__ == "__main__":
    drop_all_tables()
    create_all_tables()
    get_csv()
    create_random_orders(10)
