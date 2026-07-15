

def test_admin_dashboard_success(client, admin_token):

    response = client.get(
        "/admin",
        headers={
            "Authorization": admin_token
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "total_users" in data
    assert "total_products" in data
    assert "total_orders" in data
    assert "total_categories" in data
    assert "total_revenue" in data
    assert "pending_orders" in data
    assert "delivered_orders" in data
    assert "cancelled_orders" in data


def test_admin_dashboard_customer_forbidden(client, customer_token):

    response = client.get(
        "/admin",
        headers={
            "Authorization": customer_token
        }
    )

    assert response.status_code == 403

    data = response.get_json()

    assert data["message"] == "Only admin can access"


def test_admin_dashboard_without_token(client):

    response = client.get("/admin")

    assert response.status_code == 401

    data = response.get_json()

    assert data["message"] == "Missing or Invalid Token"