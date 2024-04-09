from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, func, DateTime
from sqlalchemy.orm import relationship
from db import db
from datetime import datetime

#Customer model
class Customer(db.Model):
    __tablename__ = 'customer'
    #define collumns for customer tabble
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False, unique=True)
    phone = Column(String(20), nullable=False)
    balance = Column(Numeric, nullable=False, default=0)
    #relationship to order model, one to many
    orders = relationship('Order', back_populates='customer')
    
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "balance": str(self.balance),
            "orders": [order.to_json() for order in self.orders]
        }
#order model
class Order(db.Model):
    __tablename__ = 'order'
    #define collumns for order table
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    customer = relationship('Customer', back_populates='orders')
    total = Column(Numeric)
    items = relationship('ProductOrder', back_populates='order', cascade="all, delete-orphan")
    created = Column(DateTime, default=func.now())
    processed = Column(DateTime, nullable=True)
    
    def get_estimated_total(self):
        total = 0 
        for item in self.items:
            total += item.product.price * item.quantity
        return total
   
    def to_json(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "total": str(self.total),
            "items": [item.to_json() for item in self.items]
        }
    
    # Processes the order based on a specified strategy.
    def process(self, strategy='adjust'):
        # Checks if order has already been processed or customer balance is insufficient.
        if self.processed:
            return False, "Order has already been processed."
        if self.customer.balance <= 0:
            return False, "Customer does not have enough balance."

        total_price = 0
        order_rejected = False

        # Loops through each item to apply the strategy.
        for item in self.items:
            available_quantity = item.product.available
            if item.quantity > available_quantity:
                if strategy == 'reject':
                    order_rejected = True
                    break  
                elif strategy == 'ignore':
                    continue 
                elif strategy == 'adjust':
                    item.quantity = available_quantity
            total_price += item.product.price * item.quantity
            item.product.available -= item.quantity
        # Handles the outcome based on the applied strategy.
        if order_rejected:
            return False, "Order rejected due to insufficient quantity for one or more products."

        if total_price > self.customer.balance:
            return False, "Not enough balance for the total order."
        # Updates the customer balance and order details, then commits the transaction.
        self.customer.balance -= total_price
        self.total = total_price
        self.processed = datetime.utcnow()  

        db.session.commit()
        return True, "Order processed successfully."

#Product Model
class Product(db.Model):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False, unique=True)
    price = Column(Numeric, nullable=False)
    available = Column(Integer, nullable=False)
    orders = relationship('ProductOrder', back_populates='product')
    
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": str(self.price),
            "available": self.available
        }

#ProductOrder Model
class ProductOrder(db.Model):
    __tablename__ = 'product_order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    order = relationship('Order', back_populates='items')
    product = relationship('Product', back_populates='orders')

    def to_json(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "product": self.product.to_json()
        }