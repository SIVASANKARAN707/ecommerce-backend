from models.cart import Cart
from extensions import db


def test_add_cart_success(client, customer_token, sample_product):

    response = client.post(
        "/carts",
        headers={
            "Authorization": customer_token
        },
        json={
            "product_id": sample_product.id,
            "quantity": 2
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["success"] is True
    assert data["message"] == "product added successfully"

    cart = Cart.query.filter_by(product_id=sample_product.id).first()

    assert cart is not None
    assert cart.quantity == 2


def test_add_cart_invalid_product(client, customer_token):

    response = client.post(
        "/carts",
        headers={
            "Authorization": customer_token
        },
        json={
            "product_id": 999,
            "quantity": 2
        }
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data["message"] == "product not found"


def test_add_cart_without_token(client, sample_product):

    response = client.post(
        "/carts",
        json={
            "product_id": sample_product.id,
            "quantity": 2
        }
    )

    assert response.status_code == 401


def test_view_cart_success(client, customer_token, customer_user, sample_product):

    cart = Cart(
        user_id=customer_user.id,
        product_id=sample_product.id,
        quantity=3
    )

    db.session.add(cart)
    db.session.commit()

    response = client.get(
        "/carts",
        headers={
            "Authorization": customer_token
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "Cart" in data
    assert isinstance(data["Cart"], list)


def test_view_cart_without_token(client):

    response = client.get("/carts")

    assert response.status_code == 401


def test_update_cart_success(client, customer_token, customer_user, sample_product):

    cart = Cart(
        user_id=customer_user.id,
        product_id=sample_product.id,
        quantity=1
    )

    db.session.add(cart)
    db.session.commit()

    response = client.put(
        f"/carts/{cart.id}",
        headers={
            "Authorization": customer_token
        },
        json={
            "quantity": 5
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "quantity updated successfully"

    updated_cart = Cart.query.get(cart.id)

    assert updated_cart.quantity == 5


def test_update_cart_not_found(client, customer_token):

    response = client.put(
        "/carts/999",
        headers={
            "Authorization": customer_token
        },
        json={
            "quantity": 5
        }
    )

    assert response.status_code == 404


def test_delete_cart_success(client, customer_token, customer_user, sample_product):

    cart = Cart(
        user_id=customer_user.id,
        product_id=sample_product.id,
        quantity=1
    )

    db.session.add(cart)
    db.session.commit()

    response = client.delete(
        f"/carts/{cart.id}",
        headers={
            "Authorization": customer_token
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "product deleted successfully"

    deleted_cart = Cart.query.get(cart.id)

    assert deleted_cart is None


def test_delete_cart_not_found(client, customer_token):

    response = client.delete(
        "/carts/999",
        headers={
            "Authorization": customer_token
        }
    )

    assert response.status_code == 404


def test_delete_cart_forbidden(client, admin_token, customer_user, sample_product):

    cart = Cart(
        user_id=customer_user.id,
        product_id=sample_product.id,
        quantity=1
    )

    db.session.add(cart)
    db.session.commit()

    response = client.delete(
        f"/carts/{cart.id}",
        headers={
            "Authorization": admin_token
        }
    )

    assert response.status_code == 403