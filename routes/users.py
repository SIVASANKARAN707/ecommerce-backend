from flask import Blueprint , request,jsonify
from extensions import db
from models.users import User
from utils.jwt_helper import token_verification

user_bp = Blueprint("user",__name__)

@user_bp.route("/users", methods=["GET"])
def get_users():
    """
Get all users
---
tags:
  - Users

parameters:
  - name: Authorization
    in: header
    type: string
    required: true
    description: JWT Token

responses:
  200:
    description: Users fetched successfully

  401:
    description: Missing or invalid token
"""
    
    decoded = token_verification()

    if not decoded:
        return jsonify({
            "success": False,
            "message":"invalid or missing token"
        }),401
    
    users = User.query.all()

    return jsonify({
        "users":[{
            "id":user.id,
            "email":user.email,
            "username":user.username} for user in users
        ]
    }),200

@user_bp.route("/users/<int:id>", methods = ["GET"])
def get_particular_user(id):
    """
Get user by ID
---
tags:
  - Users

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
    description: User fetched successfully

  401:
    description: Missing or invalid token

  404:
    description: User not found
"""

    decoded = token_verification()
    if not decoded:
        return jsonify({
            "success":False,
            "message":"invalid or missing token"
        }),401
    user = User.query.get(id)
    if user:
        return jsonify({
            "id":user.id,
            "email":user.email,
            "username":user.username

    }),200
    if not user:
        return jsonify({
            "success":False,
            "message":"user not founded"
        }),404
    

@user_bp.route("/users/<int:id>", methods = ["PUT"])
def update_user(id):
    """
Update user
---
tags:
  - Users

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
        username:
          type: string
          example: siva

        email:
          type: string
          example: siva@gmail.com

        new_password:
          type: string
          example: password123

responses:
  200:
    description: User updated successfully

  400:
    description: Invalid request

  401:
    description: Missing or invalid token

  404:
    description: User not found
"""

    decoded = token_verification()
    if not decoded:
        return jsonify({
            "success":False,
            "message":"invalid or missing token"
        }),401
    user = User.query.get(id)
    
    if not user:
        return jsonify({
            "success":False,
            "message":"user not founded"
        }),404
    data = request.json
    user.username = data.get("username",user.username)
    user.email = data.get("email",user.email)
    user.password = data.get("new_password",user.password)


    db.session.commit()

    return jsonify({
        "success": True,
        "message": "user updated successfully"
    }), 200


@user_bp.route("/users/<int:id>", methods = ["DELETE"])
def delete_user(id):
    """
Delete user
---
tags:
  - Users

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
    description: User deleted successfully

  401:
    description: Missing or invalid token

  403:
    description: Forbidden

  404:
    description: User not found
"""

    decoded = token_verification()
    if not decoded:
        return jsonify({
            "success":False,
            "message":"invalid or missing token"
        }),401
    user = User.query.get(id)
    if not user:
        return jsonify({
            "success":False,
            "message":"user not founded"
        }),404
    
    if user.id != decoded["user_id"]:
        return jsonify({"message":"forbiten"}), 403
    

    db.session.delete(user)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "user deleted successfully"
    }), 200