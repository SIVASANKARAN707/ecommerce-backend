from models.products import Product


def test_create_product_successful(
    client,
    admin_token,
    sample_category
):

    response = client.post(
        "/products",
        headers={
            "Authorization": admin_token
        },
        data={
            "product_name": "Laptop",
            "category_id": sample_category.id,
            "product_price": 100000,
            "product_description": "Gaming Laptop",
            "product_stock": 10
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert data["message"] == "product created successfully"

    product = Product.query.filter_by(
        name="Laptop"
    ).first()

    assert product is not None
    assert product.price == 100000
    assert product.stock == 10
    assert product.category_id == sample_category.id


def test_get_products(client, customer_token):

    response = client.get(
        "/products",
        headers={
            "Authorization": customer_token
        }
    )

    assert response.status_code == 200

def test_get_products_without_token(client):

    response = client.get("/products")

    assert response.status_code == 401

    data = response.get_json()

    assert data["message"] == "missing or invalid token"


def test_create_product_without_token(client, sample_category):

    response = client.post(
        "/products",
        data={
            "product_name": "Laptop",
            "category_id": sample_category.id,
            "product_price": 100000,
            "product_description": "Gaming Laptop",
            "product_stock": 10
        }
    )

    assert response.status_code == 401

def test_create_product_customer_forbidden(client, customer_token, sample_category):

    response = client.post(
        "/products",
        headers={
            "Authorization": customer_token
        },
        data={
            "product_name": "Laptop",
            "category_id": sample_category.id,
            "product_price": 100000,
            "product_description": "Gaming Laptop",
            "product_stock": 10
        }
    )

    assert response.status_code == 403


def test_create_product_missing_name(client, admin_token, sample_category):

    response = client.post(
        "/products",
        headers={
            "Authorization": admin_token
        },
        data={
            "category_id": sample_category.id,
            "product_price": 100000,
            "product_description": "Gaming Laptop",
            "product_stock": 10
        }
    )

    assert response.status_code == 400


def test_create_product_missing_category(client, admin_token):

    response = client.post(
        "/products",
        headers={
            "Authorization": admin_token
        },
        data={
            "product_name": "Laptop",
            "product_price": 100000,
            "product_description": "Gaming Laptop",
            "product_stock": 10
        }
    )

    assert response.status_code == 400


def test_create_product_invalid_category(client, admin_token):

    response = client.post(
        "/products",
        headers={
            "Authorization": admin_token
        },
        data={
            "product_name": "Laptop",
            "category_id": 999,
            "product_price": 100000,
            "product_description": "Gaming Laptop",
            "product_stock": 10
        }
    )

    assert response.status_code == 404


def test_delete_product_success(client, admin_token, sample_product):

    response = client.delete(
        f"/products/{sample_product.id}",
        headers={
            "Authorization": admin_token
        }
    )

    assert response.status_code == 200

    product = Product.query.get(sample_product.id)

    assert product is None


def test_delete_product_not_found(client, admin_token):

    response = client.delete(
        "/products/999",
        headers={
            "Authorization": admin_token
        }
    )

    assert response.status_code == 404