from flask import request , Blueprint, jsonify
from utils.jwt_helper import token_verification
from extensions import db
from models.category import Category
from models.products import Product



category_bp = Blueprint("category",__name__)

@category_bp.route("/categories",methods=["POST"])
def create_category():
    """
Create a new category
---
tags:
  - Categories

parameters:

  - name: Authorization
    in: header
    type: string
    required: true
    description: Admin JWT Token

  - name: body
    in: body
    required: true
    schema:
      properties:
        name:
          type: string
          example: Electronics

responses:

  201:
    description: Category created successfully

  400:
    description: Category already exists or invalid request

  401:
    description: Missing or invalid token

  403:
    description: Only admin can create category
"""
    decoded = token_verification()

    if not decoded:
        return jsonify({"message":"missing or invalid token"})
    if decoded["role"] != "admin":
        return jsonify({"message":"forbidden"}),403
    if decoded["role"] == "admin":
    
        data = request.json

    product_name = data.get("product_name")
    product_id = data.get("product_id")
    category_title = data.get("category_title")


    if not category_title:
        return ({"message":"title is missing"})
    
    if not product_name:
        return ({"message":"product_name is missing"})
    
    new_category = Category(
        name=category_title
        )   
    db.session.add(new_category)
    db.session.commit()

    return jsonify({"message":"category created successfully"}),200


@category_bp.route("/categories/<int:id>",methods=["PUT"])
def update_category(id):
    """
Update category
---
tags:
  - Categories

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
        name:
          type: string
          example: Home Appliances

responses:

  200:
    description: Category updated successfully

  400:
    description: Invalid request

  401:
    description: Missing or invalid token

  403:
    description: Only admin can update category

  404:
    description: Category not found
"""
    decoded = token_verification()

    if not decoded:
        return jsonify({"message":"missing or invalid token"})
    if decoded["role"] != "admin":
        return jsonify({"message":"forbidden"}),403
    if decoded["role"] == "admin":
    
        data = request.json

    product_name = data.get("product.name")
    category_title = data.get("catagory_title")


    if not category_title:
        return ({"message":"title is missing"})
    if not product_name:
        return ({"message":"product_name is missing"})
    
    db.session.commit()

    return jsonify({"message":"category updated successfully"}),200


@category_bp.route("/categories/<int:id>",methods=["DELETE"])
def delete_category(id):
    """
Delete category
---
tags:
  - Categories

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

responses:

  200:
    description: Category deleted successfully

  401:
    description: Missing or invalid token

  403:
    description: Only admin can delete category

  404:
    description: Category not found
"""
    decoded = token_verification()

    if not decoded:
        return jsonify({"message":"missing or invalid token"})
    if decoded["role"] != "admin":
        return jsonify({"message":"forbidden"}),403
    if decoded["role"] == "admin":
        category = Category.query.get(id)
        if not category:
            return jsonify({
            "success": False,
            "message": "product not found"
        }), 404


        db.session.delete(Category)
        db.session.commit()

        return jsonify({"message":"category deleted successfully"}),200


@category_bp.route("/categories/<int:id>",methods=["GET"])
def select_particular_catagory(id):
    """
Get category by ID
---
tags:
  - Categories

parameters:

  - name: Authorization
    in: header
    type: string
    required: true

  - name: id
    in: path
    type: integer
    required: true
    example: 1

responses:

  200:
    description: Category fetched successfully

  401:
    description: Missing or invalid token

  404:
    description: Category not found
"""
    decoded = token_verification()

    if not decoded:
        return jsonify({"message":"missing or invalid token"})
        
    category = Category.query.filter_by(user_id=decoded["user_id"]).all()
    category = Category.query.get(id)
    if not category:
            return jsonify({
            "success": False,
            "message": "product not found"
    }), 404


    return jsonify({
            "Category": [{
            "category_title":category.title,
            "category_id":category.id}for category in category]
        }),200



@category_bp.route("/categories",methods=["GET"])
def view_all_category():
    """
Get all categories
---
tags:
  - Categories

parameters:

  - name: Authorization
    in: header
    type: string
    required: true
    description: JWT Token

responses:

  200:
    description: Categories fetched successfully

  401:
    description: Missing or invalid token
"""
    decoded = token_verification()

    if not decoded:
        return jsonify({"message":"missing or invalid token"})
        
    category = Category.query.filter_by(user_id=decoded["user_id"]).all()
    category = Category.query.all()


    return jsonify({
            "Category": [{
            "category_title":category.title,
            "category_id":category.id}for category in category]
        }),200

