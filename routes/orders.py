from flask import request, jsonify, Blueprint
from extensions import db

from utils.jwt_helper import token_verification

from models.cart import Cart
from models.orderitem import OrderItem
from models.products import Product
from models.order import Order


orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/checkout",methods=["POST"])
def checkout():
    """
Checkout Cart
---
tags:
  - Orders

summary: Place a new order

description: >
  Creates an order from all items in the authenticated user's cart,
  reduces product stock, creates order items, and clears the cart.

parameters:
  - name: Authorization
    in: header
    type: string
    required: true
    description: JWT Token

responses:
  201:
    description: Order placed successfully

  400:
    description: Cart is empty or product is out of stock

  401:
    description: Missing or invalid token
"""
    decoded = token_verification()

    if not decoded:
        return jsonify({"message":"missing or invalid token"}), 401


    cart_items = Cart.query.filter_by(
    user_id=decoded["user_id"]
).all()
    

    if not cart_items:
        return jsonify ({"message":"cart is empty"}), 400
    

    total_price = 0

    for item in cart_items:
        product = Product.query.get(item.product_id)
        total_price += product.price * item.quantity
    
    #check stock
    for item in cart_items:
        product = Product.query.get(item.product_id)
        if product.stock < item.quantity:
            return jsonify({
            "success": False,
            "message": f"{product.name} is out of stock"
        }), 400

    #crete order
    order = Order(
    user_id=decoded["user_id"],
    total_price=total_price,
    status="Pending"
)

    db.session.add(order)

    db.session.flush()

    #create orderitem

    for item in cart_items:

        product = Product.query.get(item.product_id)

        order_item = OrderItem(

        order_id=order.id,

        product_id=product.id,

        quantity=item.quantity,

        price=product.price
    )

        db.session.add(order_item)


    #reduce stock
    for item in cart_items:

        product = Product.query.get(item.product_id)

        product.stock -= item.quantity

    #clear cart
    for item in cart_items:

        db.session.delete(item)
    db.session.commit()


    #return response
    return jsonify({

    "success": True,

    "message": "Order placed successfully",

    "order_id": order.id

}), 201

@orders_bp.route("/orders", methods=["GET"])
def get_orders():
    """
Get Orders
---
tags:
  - Orders

summary: Get all orders

description: >
  Admin users receive all orders.
  Customers receive only their own orders.

parameters:
  - name: Authorization
    in: header
    type: string
    required: true
    description: JWT Token

responses:
  200:
    description: Orders fetched successfully

  401:
    description: Missing or invalid token
"""

    decoded = token_verification()

    if not decoded:
        return jsonify({"message": "Missing or Invalid Token"}), 401

    if decoded["role"] == "admin":
        orders = Order.query.all()
    else:
        orders = Order.query.filter_by(user_id=decoded["user_id"]).all()

    return jsonify({
        "orders": [
            {
                "id": order.id,
                "total_price": order.total_price,
                "status": order.status,
                "created_at": order.created_at,
                "user_id": order.user_id
            }
            for order in orders
        ]
    }), 200

@orders_bp.route("/orders/<int:id>", methods=["GET"])
def get_order(id):
    """
Get Order By ID
---
tags:
  - Orders

summary: Get a specific order

parameters:
  - name: Authorization
    in: header
    type: string
    required: true
    description: JWT Token

  - name: id
    in: path
    type: integer
    required: true
    example: 1

responses:
  200:
    description: Order fetched successfully

  401:
    description: Missing or invalid token

  403:
    description: Forbidden

  404:
    description: Order not found
"""

    decoded = token_verification()

    if not decoded:
        return jsonify({"message": "Missing or Invalid Token"}), 401

    order = Order.query.get(id)

    if not order:
        return jsonify({
            "message": "Order not found"
        }),404

    if decoded["role"] != "admin" and order.user_id != decoded["user_id"]:
        return jsonify({
            "message":"Forbidden"
        }),403

    return jsonify({
        "id": order.id,
        "total_price": order.total_price,
        "status": order.status,
        "created_at": order.created_at,
        "user_id": order.user_id
    }),200

@orders_bp.route("/orders/<int:id>", methods=["PUT"])
def update_order(id):
    """
Update Order Status
---
tags:
  - Orders

summary: Update order status

description: >
  Only admin users can update an order status.

parameters:
  - name: Authorization
    in: header
    type: string
    required: true
    description: Admin JWT Token

  - name: id
    in: path
    type: integer
    required: true
    example: 1

  - name: body
    in: body
    required: true
    schema:
      properties:
        status:
          type: string
          example: Delivered

responses:
  200:
    description: Order updated successfully

  401:
    description: Missing or invalid token

  403:
    description: Only admin can update orders

  404:
    description: Order not found
"""

    decoded = token_verification()

    if not decoded:
        return jsonify({"message":"Missing or Invalid Token"}),401

    if decoded["role"] != "admin":
        return jsonify({"message":"Forbidden"}),403

    order = Order.query.get(id)

    if not order:
        return jsonify({
            "message":"Order not found"
        }),404

    data = request.json

    order.status = data.get("status", order.status)

    db.session.commit()

    return jsonify({
        "message":"Order updated successfully"
    }),200


@orders_bp.route("/orders/<int:id>", methods=["DELETE"])
def delete_order(id):
    """
Delete Order
---
tags:
  - Orders

summary: Delete an order

description: >
  Admin users can delete any order.
  Customers can delete only their own orders.

parameters:
  - name: Authorization
    in: header
    type: string
    required: true
    description: JWT Token

  - name: id
    in: path
    type: integer
    required: true
    example: 1

responses:
  200:
    description: Order deleted successfully

  401:
    description: Missing or invalid token

  403:
    description: Forbidden

  404:
    description: Order not found
"""

    decoded = token_verification()

    if not decoded:
        return jsonify({"message":"Missing or Invalid Token"}),401

    order = Order.query.get(id)

    if not order:
        return jsonify({
            "message":"Order not found"
        }),404

    if decoded["role"] != "admin" and order.user_id != decoded["user_id"]:
        return jsonify({
            "message":"Forbidden"
        }),403

    db.session.delete(order)
    db.session.commit()

    return jsonify({
        "message":"Order deleted successfully"
    }),200