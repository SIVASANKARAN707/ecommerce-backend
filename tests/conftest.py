import pytest

from create_app import create_app
from extensions import db

import bcrypt
import jwt

import os

from models.users import User
from models.category import Category
from models.products import Product

from models.cart import Cart


@pytest.fixture
def app():

    app = create_app(TestingConfig)

    with app.app_context():

        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def customer_user(app):

    hashed_password = bcrypt.hashpw(
        "password123".encode(),
        bcrypt.gensalt()
    ).decode()

    user = User(
        username="customer",
        email="customer@test.com",
        password=hashed_password,
        role="customer"
    )

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def admin_user(app):

    hashed_password = bcrypt.hashpw(
        "admin123".encode(),
        bcrypt.gensalt()
    ).decode()

    user = User(
        username="admin",
        email="admin@test.com",
        password=hashed_password,
        role="admin"
    )

    db.session.add(user)
    db.session.commit()

    return user

from config import TestingConfig

@pytest.fixture
def customer_token(customer_user):

    return jwt.encode(
        {
            "user_id": customer_user.id,
            "role": customer_user.role
        },
        os.getenv("JWT_SECRET"),
        algorithm="HS256"
    )


@pytest.fixture
def admin_token(admin_user):

    return jwt.encode(
        {
            "user_id": admin_user.id,
            "role": admin_user.role
        },
        os.getenv("JWT_SECRET"),
        algorithm="HS256"
    )


@pytest.fixture
def sample_category(app):

    category = Category(
        name="Electronics"
    )

    db.session.add(category)
    db.session.commit()

    return category


@pytest.fixture
def sample_product(app, sample_category):

    product = Product(
        name="Laptop",
        description="Gaming Laptop",
        price=50000,
        stock=10,
        image="default.jpg",
        category_id=sample_category.id
    )

    db.session.add(product)
    db.session.commit()

    return product


@pytest.fixture
def sample_cart(customer_user, sample_product):

    cart = Cart(
        user_id=customer_user.id,
        product_id=sample_product.id,
        quantity=2
    )

    db.session.add(cart)
    db.session.commit()

    return cart