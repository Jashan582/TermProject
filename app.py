
from flask import Flask
from pathlib import Path
from db import db
from routes import api_customers_bp, api_orders_bp, api_products_bp, url_bp

#create instance of the flask class
app = Flask(__name__)
#configure the Flask app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///i_copy_pasted_this.db"
app.config['SECRET_KEY'] = 'your_really_secret_key_here'
app.config['SESSION_COOKIE_SECURE'] = True
app.instance_path = Path("change_this").resolve()
db.init_app(app)


#register blueprints with application
app.register_blueprint(api_customers_bp, url_prefix="/api/customers")
app.register_blueprint(api_orders_bp, url_prefix="/api/orders")
app.register_blueprint(api_products_bp, url_prefix="/api/products")
app.register_blueprint(url_bp) 

if __name__ == '__main__':
    app.run(debug=True)
