from flask import Flask, send_from_directory
from flask_migrate import Migrate

from config import Config
from extensions import db

# Import Models
from models.order import Order
from models.orderitem import OrderItem
from models.cart import Cart
from models.category import Category
from models.products import Product
from models.users import User

# Import Blueprints
from routes.users import user_bp
from routes.products import products_bp
from routes.cart import cart_bp
from routes.auth import auth_bp
from routes.category import category_bp
from routes.orders import orders_bp
from routes.admin import admin_bp

migrate = Migrate()


def create_app(config_class=Config):

    app = Flask(__name__)

    app.config.from_object(config_class)

    db.init_app(app)

    migrate.init_app(app, db)

    app.register_blueprint(user_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(admin_bp)

    @app.route("/uploads/products/<filename>")
    def uploaded_file(filename):
        return send_from_directory(
            "uploads/products",
            filename
        )

    return app