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
    """
Admin Dashboard
---
tags:
  - Admin

summary: Get admin dashboard statistics

description: >
  Returns dashboard statistics including total users, products,
  categories, orders, revenue and order status counts.
  Accessible only by admin users.

parameters:
  - name: Authorization
    in: header
    type: string
    required: true
    description: Admin JWT Token

responses:

  200:
    description: Dashboard data retrieved successfully
    schema:
      type: object
      properties:
        total_users:
          type: integer
          example: 25

        total_products:
          type: integer
          example: 120

        total_categories:
          type: integer
          example: 8

        total_orders:
          type: integer
          example: 60

        total_revenue:
          type: integer
          example: 350000

        pending_orders:
          type: integer
          example: 10

        delivered_orders:
          type: integer
          example: 45

        cancelled_orders:
          type: integer
          example: 5

  401:
    description: Missing or invalid token
    schema:
      properties:
        message:
          type: string
          example: Missing or Invalid Token

  403:
    description: Only admin can access this endpoint
    schema:
      properties:
        message:
          type: string
          example: only admin can access
"""

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