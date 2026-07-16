from flask import request ,Blueprint,jsonify
import bcrypt
import os
import jwt
from extensions import db
from models.users import User


auth_bp = Blueprint("auth",__name__)

@auth_bp.route("/register", methods = ["POST"])
def register():

    """
Register a new user
---
tags:
  - Authentication

parameters:
  - in: body
    name: body
    required: true
    schema:
      properties:
        username:
          type: string
          example: siva
        email: 
          type: string
          example: siva@gmail.com
        password:
          type: string
          example: "1234"

responses:
  200:
    description: User registered successfully

  400:
    description: Invalid request
"""


    data = request.json

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    if not username:
        return jsonify({
        "message":"missing name"
    }),400
    if not password:
        return jsonify({
        "message":"missing password"}),400
    if not email:
        return jsonify({
            "message":"missing email"
        }),400
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({
            "message":"username already exists"
        }),400 
    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        return jsonify({
            "message":"email is already exists"
        }),400
    
    hashed = bcrypt.hashpw(
    password.encode(),
    bcrypt.gensalt()
    ).decode()

    user = User(
        username=username,
        password=hashed,
        email=email,
        role = "customer"
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"message" : f"User {username} register successfully"}),201


@auth_bp.route("/login",methods=["POST"])
def login():


    """
User Login
---
tags:
  - Authentication

parameters:
  - in: body
    name: body
    required: true
    schema:
      properties:
        email:
          type: string
          example: siva@gmail.com
        password:
          type: string
          example: "1234"

responses:
  200:
    description: Login successful
    schema:
      properties:
        success:
          type: boolean
          example: true
        token:
          type: string
          example: eyJhbGciOiJIUzI1NiIs...

  401:
    description: Invalid username or password
"""


    data = request.json

    email = data.get("email")
    enter_password = data.get("password")

    if not email:
        return jsonify ({"message":"missing email"}),400
    
    if not enter_password:
        return jsonify({"message":"missing password"}),400
    
    user = User.query.filter_by(email=email).first()

    if user and bcrypt.checkpw(enter_password.encode(),user.password.encode()):
        token = jwt.encode({"user_id":user.id,
                            "role":user.role},
                           os.getenv("JWT_SECRET"),
                           algorithm = "HS256")
        return jsonify ({"message":"Login successful",
                        "success":True,
                        "token":token}),200
    
    return jsonify({
        "message":"Invalid email or password",
        "success":False
    }),401
    
