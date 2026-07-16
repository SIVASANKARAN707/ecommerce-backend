from flask import Blueprint, request, jsonify
from extensions import db
from models.category import Category
from utils.jwt_helper import token_verification

category_bp = Blueprint("category", __name__)


@category_bp.route("/categories", methods=["POST"])
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
        return jsonify({"message": "Missing or Invalid Token"}), 401

    if decoded["role"] != "admin":
        return jsonify({"message": "Forbidden"}), 403

    data = request.json

    name = data.get("name")

    if not name:
        return jsonify({
            "message": "name is missing"
        }), 400

    existing_category = Category.query.filter_by(name=name).first()

    if existing_category:
        return jsonify({
            "message": "Category already exists"
        }), 400

    category = Category(name=name)

    db.session.add(category)
    db.session.commit()

    return jsonify({
        "message": "Category created successfully"
    }), 201


@category_bp.route("/categories", methods=["GET"])
def get_categories():
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
        return jsonify({"message": "Missing or Invalid Token"}), 401

    categories = Category.query.all()

    return jsonify({
        "categories": [
            {
                "id": category.id,
                "name": category.name
            }
            for category in categories
        ]
    }), 200


@category_bp.route("/categories/<int:id>", methods=["GET"])
def get_category(id):
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
        return jsonify({"message": "Missing or Invalid Token"}), 401

    category = Category.query.get(id)

    if not category:
        return jsonify({
            "message": "Category not found"
        }), 404

    return jsonify({
        "id": category.id,
        "name": category.name
    }), 200


@category_bp.route("/categories/<int:id>", methods=["PUT"])
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
        return jsonify({"message": "Missing or Invalid Token"}), 401

    if decoded["role"] != "admin":
        return jsonify({"message": "Forbidden"}), 403

    category = Category.query.get(id)

    if not category:
        return jsonify({
            "message": "Category not found"
        }), 404

    data = request.json

    name = data.get("name")

    if not name:
        return jsonify({
            "message": "name is missing"
        }), 400

    category.name = name

    db.session.commit()

    return jsonify({
        "message": "Category updated successfully"
    }), 200


@category_bp.route("/categories/<int:id>", methods=["DELETE"])
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
        return jsonify({"message": "Missing or Invalid Token"}), 401

    if decoded["role"] != "admin":
        return jsonify({"message": "Forbidden"}), 403

    category = Category.query.get(id)

    if not category:
        return jsonify({
            "message": "Category not found"
        }), 404

    db.session.delete(category)
    db.session.commit()

    return jsonify({
        "message": "Category deleted successfully"
    }), 200