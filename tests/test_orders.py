from models.cart import Cart
from models.order import Order
from models.products import Product
from extensions import db


def test_checkout_success(client, customer_token, customer_user, sample_product):

    cart = Cart(
        user_id=customer_user.id,
        product_id=sample_product.id,
        quantity=2
    )

    db.session.add(cart)
    db.session.commit()

    response = client.post(
        "/checkout",
        headers={
            "Authorization": customer_token
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["success"] is True
    assert data["message"] == "Order placed successfully"

    order = Order.query.get(data["order_id"])

    assert order is not None


def test_checkout_empty_cart(client, customer_token):

    response = client.post(
        "/checkout",
        headers={
            "Authorization": customer_token
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["message"] == "cart is empty"


def test_checkout_insufficient_stock(client, customer_token, customer_user, sample_product):

    sample_product.stock = 1
    db.session.commit()

    cart = Cart(
        user_id=customer_user.id,
        product_id=sample_product.id,
        quantity=5
    )

    db.session.add(cart)
    db.session.commit()

    response = client.post(
        "/checkout",
        headers={
            "Authorization": customer_token
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert "out of stock" in data["message"]


def test_get_orders_customer(client, customer_token):

    response = client.get(
        "/orders",
        headers={
            "Authorization": customer_token
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "orders" in data


def test_get_orders_admin(client, admin_token):

    response = client.get(
        "/orders",
        headers={
            "Authorization": admin_token
        }
    )

    assert response.status_code == 200


def test_get_orders_without_token(client):

    response = client.get("/orders")

    assert response.status_code == 401


def test_get_single_order_success(client, customer_token, customer_user):

    order = Order(
        user_id=customer_user.id,
        total_price=1000,
        status="Pending"
    )

    db.session.add(order)
    db.session.commit()

    response = client.get(
        f"/orders/{order.id}",
        headers={
            "Authorization": customer_token
        }
    )

    assert response.status_code == 200


def test_get_single_order_not_found(client, customer_token):

    response = client.get(
        "/orders/999",
        headers={
            "Authorization": customer_token
        }
    )

    assert response.status_code == 404


def test_update_order_success(client, admin_token, customer_user):

    order = Order(
        user_id=customer_user.id,
        total_price=1000,
        status="Pending"
    )

    db.session.add(order)
    db.session.commit()

    response = client.put(
        f"/orders/{order.id}",
        headers={
            "Authorization": admin_token
        },
        json={
            "status": "Delivered"
        }
    )

    assert response.status_code == 200

    updated = Order.query.get(order.id)

    assert updated.status == "Delivered"


def test_update_order_customer_forbidden(client, customer_token, customer_user):

    order = Order(
        user_id=customer_user.id,
        total_price=1000,
        status="Pending"
    )

    db.session.add(order)
    db.session.commit()

    response = client.put(
        f"/orders/{order.id}",
        headers={
            "Authorization": customer_token
        },
        json={
            "status": "Delivered"
        }
    )

    assert response.status_code == 403


def test_delete_order_success(client, customer_token, customer_user):

    order = Order(
        user_id=customer_user.id,
        total_price=1000,
        status="Pending"
    )

    db.session.add(order)
    db.session.commit()

    response = client.delete(
        f"/orders/{order.id}",
        headers={
            "Authorization": customer_token
        }
    )

    assert response.status_code == 200

    deleted = Order.query.get(order.id)

    assert deleted is None


def test_delete_order_not_found(client, customer_token):

    response = client.delete(
        "/orders/999",
        headers={
            "Authorization": customer_token
        }
    )

    assert response.status_code == 404