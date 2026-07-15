from flask import request , Blueprint, jsonify
from utils.jwt_helper import token_verification
from extensions import db
from models.category import Category
from models.products import Product



category_bp = Blueprint("category",__name__)

@category_bp.route("/categories",methods=["POST"])
def create_category():
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

