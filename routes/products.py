from flask import request, Blueprint,jsonify
from extensions import db
import os
from utils.jwt_helper import token_verification
from models.products import Product
from models.category import Category
from werkzeug.utils import secure_filename

import uuid





products_bp = Blueprint("products",__name__)
UPLOAD_FOLDER = "uploads/products"
ALLOWED_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp"
}

def allowed_file(filename):

    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@products_bp.route("/products", methods=["GET"])
def get_products():

    """
Get all products
---
tags:
  - Products

parameters:

  - name: Authorization
    in: header
    type: string
    required: true
    description: JWT Token

  - name: search
    in: query
    type: string
    required: false
    example: laptop

  - name: category
    in: query
    type: integer
    required: false
    example: 1

  - name: page
    in: query
    type: integer
    required: false
    example: 1

  - name: limit
    in: query
    type: integer
    required: false
    example: 10

  - name: sort
    in: query
    type: string
    required: false
    enum:
      - price
      - -price

responses:

  200:
    description: Products fetched successfully

  401:
    description: Missing or invalid token
"""
    decoded = token_verification()

    if not decoded:
        return jsonify({"message": "missing or invalid token"}), 401
    query = Product.query
    
    search = request.args.get("search")
    category = request.args.get("category")
    page = request.args.get("page",1,type=int)
    limit = request.args.get("limit",10,type=int)
    sort = request.args.get("sort")

    if search:
        query = query.filter(
    Product.name.ilike(f"%{search}%")
)
    
                            
    if category:
        query = query.filter(
            Product.category_id == category
        )
    if sort == "price":
        query = query.order_by(
    Product.price.asc()
    )
    elif sort == "-price":
        query = query.order_by(Product.price.desc())
        
    products = query.paginate(
    page=page,
    per_page=limit,
    error_out=False
    )
    return jsonify({
        "Products": [
            {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "description": product.description,
                "category": product.category.name if product.category else None,
                "image": f"/uploads/products/{product.image}"if product.image else None
            }
            for product in products.items
        ]
    }), 200


@products_bp.route("/products/<int:id>",methods=["GET"])
def get_product(id):
    """
Get product by ID
---
tags:
  - Products

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
    description: Product fetched successfully

  401:
    description: Missing or invalid token

  404:
    description: Product not found
"""
    decoded = token_verification()

    if not decoded:
        return jsonify({"message":"missing or invalid token"})
    
    product = Product.query.get(id)

    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description,
            "category": product.category.name if product.category else None,
            "image": f"/uploads/products/{product.image}"

    }),200
    if not product:
        return jsonify({
            "success":False,
            "message":"product not founded"
        }),404
    

@products_bp.route("/products/<int:id>", methods =["PUT"])
def update_product(id):
    """
Update product
---
tags:
  - Products

consumes:
  - multipart/form-data

parameters:

  - name: Authorization
    in: header
    type: string
    required: true

  - name: id
    in: path
    type: integer
    required: true

  - name: product_name
    in: formData
    type: string

  - name: product_price
    in: formData
    type: integer

  - name: product_description
    in: formData
    type: string

  - name: product_stock
    in: formData
    type: integer

  - name: category_id
    in: formData
    type: integer

  - name: image
    in: formData
    type: file

responses:

  200:
    description: Product updated successfully

  401:
    description: Missing or invalid token

  403:
    description: Only admin can update products

  404:
    description: Product not found
"""


    decoded = token_verification()

    if not decoded:
        return jsonify({"message":"missing or invalid token"})
    if decoded["role"] != "admin":
        return jsonify({"message":"forbidden"}),403
    if decoded["role"] == "admin":

        product = Product.query.get(id)
        if not product:
            return jsonify({
            "success": False,
            "message": "product not found"
        }), 404

        data = request.json

        product.name = data.get("product_name", product.name)
        product.price = data.get("product_price",product.price)


        db.session.commit()

        return jsonify({
        "success": True,
        "message": "product updated successfully"
    }), 200


@products_bp.route("/products", methods =["POST"])
    

def create_product():
    """
Create a new product
---
tags:
  - Products

consumes:
  - multipart/form-data

parameters:
  - name: Authorization
    in: header
    type: string
    required: true
    description: JWT token of an admin user
    example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4ifQ.0noGoFDsTlDhfaYt2tbjBBCFT7lM5hhvUjhLoACAqzA"

  - name: product_name
    in: formData
    type: string
    required: true
    example: Laptop

  - name: category_id
    in: formData
    type: integer
    required: true
    example: 1

  - name: product_price
    in: formData
    type: integer
    required: true
    example: 75000

  - name: product_description
    in: formData
    type: string
    required: false
    example: Gaming Laptop with RTX graphics

  - name: product_stock
    in: formData
    type: integer
    required: true
    example: 10

  - name: image
    in: formData
    type: file
    required: false
    description: JPG, JPEG, PNG or WEBP image

responses:
  200:
    description: Product created successfully
    schema:
      properties:
        success:
          type: boolean
          example: true
        message:
          type: string
          example: product created successfully

  400:
    description: Validation error
    schema:
      properties:
        message:
          type: string
          example: category_id is required

  401:
    description: Missing or invalid token
    schema:
      properties:
        message:
          type: string
          example: missing or invalid token

  403:
    description: Only admin can create products
    schema:
      properties:
        message:
          type: string
          example: forbidden

  404:
    description: Category not found
    schema:
      properties:
        message:
          type: string
          example: Category not found
"""
    decoded = token_verification()

    if not decoded:
        return jsonify({"message":"missing or invalid token"}), 401
    if decoded["role"] != "admin":
        return jsonify({"message":"forbidden"}),403
    if decoded["role"] == "admin":

        
        name = request.form.get("product_name")

        category_id = request.form.get("category_id")

        price = request.form.get("product_price")

        description = request.form.get("product_description")

        stock = request.form.get("product_stock")

        image = request.files.get("image")

    

    if not name:
        return jsonify({"message": "product_name is required"}), 400

    if not price:
        return jsonify({"message": "product_price is required"}), 400

    if not stock:
        return jsonify({"message": "product_stock is required"}), 400
    if not category_id:
        return jsonify({"message": "category_id is required"}), 400


    filename = "default.jpg"

    
    if image:

        if not allowed_file(image.filename):

            return jsonify({
            "success": False,
            "message": "Only JPG, JPEG, PNG and WEBP images are allowed"
            }),400
        
        extension = image.filename.rsplit(".",1)[1].lower()

        filename = f"{uuid.uuid4()}.{extension}"

        image.save(
        os.path.join(UPLOAD_FOLDER, filename)
    )
    else:
        filename = "default.jpg"
        



    category = Category.query.get(category_id)

    if not category:
            return jsonify({
            "message":"Category not found"
        }),404
        
    new_product = Product (
    name=name,
    description=description,
    price=price,
    stock=stock,
    category_id=category_id,
    image=filename
)

    db.session.add(new_product)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "product created successfully"
    }), 200



@products_bp.route("/products/<int:id>", methods =["DELETE"])
def delete_product(id):
    """
Delete product
---
tags:
  - Products

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
    description: Product deleted successfully

  401:
    description: Missing or invalid token

  403:
    description: Only admin can delete products

  404:
    description: Product not found
"""
    decoded = token_verification()

    if not decoded:
        return jsonify({"message":"missing or invalid token"})
    if decoded["role"] != "admin":
        return jsonify({"message":"forbidden"}),403
    if decoded["role"] == "admin":

        product = Product.query.get(id)
        if not product:
            return jsonify({
            "success": False,
            "message": "product not found"
        }), 404

        db.session.delete(product)
        db.session.commit()

        return jsonify({
        "success": True,
        "message": "product deleted successfully"
    }),200
