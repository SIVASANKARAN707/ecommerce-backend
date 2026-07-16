from flask import request , Blueprint, jsonify
from utils.jwt_helper import token_verification
from extensions import db
from models.cart import Cart
from models.products import Product


cart_bp = Blueprint("cart",__name__)


@cart_bp.route("/carts",methods =["POST"])
def add_cart():
    """
Add product to cart
---
tags:
  - Cart

parameters:
  - name: Authorization
    in: header
    type: string
    required: true
    description: JWT Token

  - name: body
    in: body
    required: true
    schema:
      properties:
        product_id:
          type: integer
          example: 1

        quantity:
          type: integer
          example: 2

responses:
  201:
    description: Product added to cart successfully

  400:
    description: Invalid request

  401:
    description: Missing or invalid token

  404:
    description: Product not found
"""
    decoded = token_verification()

    if not decoded:
        return jsonify({"message":"missing or invalid token"}),401
    
    data = request.json

    
    product_id= data.get("product_id")
    quantity= data.get("quantity")

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message":"product not found"}),404
    
    new_cart = Cart(
    user_id=decoded["user_id"],
    product_id=product_id,
    quantity=quantity
)

    db.session.add(new_cart)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "product added successfully"
    }),201



@cart_bp.route("/carts",methods=["GET"])
def view_carts():
    """
View cart
---
tags:
  - Cart

parameters:
  - name: Authorization
    in: header
    type: string
    required: true
    description: JWT Token

responses:
  200:
    description: Cart fetched successfully

  401:
    description: Missing or invalid token
"""
    decoded = token_verification()

    if not decoded:
        return jsonify({"message":"missing or invalid token"}), 401
    
    carts = Cart.query.filter_by(user_id=decoded["user_id"]).all()

    return jsonify({
            "Cart": [{
            "name":cart.product.name,
            "price":cart.product.price,
            "quantity":cart.quantity}for cart in carts]
        }),200


@cart_bp.route("/carts/<int:id>",methods=["PUT"])
def update_carts(id):
    """
Update cart quantity
---
tags:
  - Cart

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

  - name: body
    in: body
    required: true
    schema:
      properties:
        quantity:
          type: integer
          example: 5

responses:
  200:
    description: Quantity updated successfully

  401:
    description: Missing or invalid token

  403:
    description: Forbidden

  404:
    description: Cart item not found
"""
    decoded = token_verification()

    if not decoded:
        return jsonify({"message":"missing or invalid token"}), 401
    
    cart = Cart.query.get(id)
    if not cart:
            return jsonify({
            "success": False,
            "message": "product not found"
        }), 404
    
    if cart.user_id != decoded["user_id"]:
        return jsonify({"message":"forbidden"}),403
    

    if cart.user_id == decoded["user_id"]:

        

        data= request.json

        cart.quantity = data.get("quantity")


        db.session.commit()

        return jsonify({
        "success": True,
        "message": "quantity updated successfully"
    }), 200

@cart_bp.route("/carts/<int:id>", methods =["DELETE"])
def delete_cart(id):
    """
Delete cart item
---
tags:
  - Cart

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
    description: Product removed from cart successfully

  401:
    description: Missing or invalid token

  403:
    description: Forbidden

  404:
    description: Cart item not found
"""
    decoded = token_verification()

    if not decoded:
        return jsonify({"message":"missing or invalid token"}), 401
    
    cart = Cart.query.get(id)
    if not cart:
            return jsonify({
            "success": False,
            "message": "product not found"
        }), 404

    if cart.user_id != decoded["user_id"]:
        return jsonify({"message":"forbidden"}),403
    

    if  cart.user_id == decoded["user_id"]:

        db.session.delete(cart)
        db.session.commit()

        return jsonify({
        "success": True,
        "message": "product deleted successfully"
    }),200
