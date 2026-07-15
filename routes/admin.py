from flask import request, Blueprint,jsonify
from extensions import db
from utils.jwt_helper import token_verification
from models.products import Product
from models.category import Category
from models.users import User
from models.order import Order

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin",methods =["GET"])
def view_dashboard():

    decoded = token_verification()

    if not decoded:
        return jsonify({"message": "Missing or Invalid Token"}), 401

    if decoded["role"] != "admin":
        return jsonify({"message":"Only admin can access"}),403
    
    total_users = User.query.count()

    total_products = Product.query.count()

    total_orders = Order.query.count()

    total_categories = Category.query.count()


    orders = Order.query.all()

    revenue = sum(order.total_price for order in orders)

    pending_orders = Order.query.filter_by(
    status="Pending"
    ).count()

    delivered_orders = Order.query.filter_by(
    status="Delivered"
    ).count()

    cancelled_orders = Order.query.filter_by(
    status="Cancelled"
    ).count()

    return jsonify({
    "total_users": total_users,
    "total_products": total_products,
    "total_orders": total_orders,
    "total_categories": total_categories,
    "total_revenue": revenue,
    "pending_orders": pending_orders,
    "delivered_orders": delivered_orders,
    "cancelled_orders": cancelled_orders
}), 200