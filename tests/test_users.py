from models.users import User


def test_get_users_success(client, customer_token, customer_user):

    response = client.get(
        "/users",
        headers={
            "Authorization": customer_token
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "users" in data
    assert isinstance(data["users"], list)


def test_get_users_without_token(client):

    response = client.get("/users")

    assert response.status_code == 401

    data = response.get_json()

    assert data["message"] == "invalid or missing token"


def test_get_single_user_success(client, customer_token, customer_user):

    response = client.get(
        f"/users/{customer_user.id}",
        headers={
            "Authorization": customer_token
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["email"] == customer_user.email
    assert data["username"] == customer_user.username


def test_get_single_user_not_found(client, customer_token):

    response = client.get(
        "/users/999",
        headers={
            "Authorization": customer_token
        }
    )

    assert response.status_code == 404


def test_update_user_success(client, customer_token, customer_user):

    response = client.put(
        f"/users/{customer_user.id}",
        headers={
            "Authorization": customer_token
        },
        json={
            "username": "updated_user",
            "email": "updated@test.com",
            "new_password": "newpassword123"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "user updated successfully"

    user = User.query.get(customer_user.id)

    assert user.username == "updated_user"
    assert user.email == "updated@test.com"


def test_update_user_not_found(client, customer_token):

    response = client.put(
        "/users/999",
        headers={
            "Authorization": customer_token
        },
        json={
            "username": "updated"
        }
    )

    assert response.status_code == 404


def test_delete_user_success(client, customer_token, customer_user):

    response = client.delete(
        f"/users/{customer_user.id}",
        headers={
            "Authorization": customer_token
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "user deleted successfully"

    user = User.query.get(customer_user.id)

    assert user is None


def test_delete_user_unauthorized(client, customer_user, admin_token):

    response = client.delete(
        f"/users/{customer_user.id}",
        headers={
            "Authorization": admin_token
        }
    )

    assert response.status_code == 403


def test_delete_user_without_token(client, customer_user):

    response = client.delete(
        f"/users/{customer_user.id}"
    )

    assert response.status_code == 401

