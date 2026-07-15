from models.users import User


def test_register_successfully(client):

    response = client.post(
        "/register",
        json = {
            "username":"siva",
            "email":"siva@gmail.com",
            "password":"1234"
        }
    )
    assert response.status_code == 201

    data = response.get_json()

    assert data["message"] == "User siva register successfully"

    user = User.query.filter_by(email="siva@gmail.com").first()
    assert user  is not None
    assert user.username == "siva"


def test_login_success(client,customer_user):

    response = client.post(
        "/login",
        json = {
            "email":"customer@test.com",
            "password":"password123"
        }
    )
    assert response.status_code == 200

    data = response.get_json()

    assert "token" in data

    assert data["message"] == "Login successful"

def test_login_fail_wrong_password(client,customer_user):
    response = client.post("/login", 
        json={"email": "customer@test.com", "password": "wrong_password"})

    assert response.status_code == 401
    data = response.get_json()

    assert data["message"] == "Invalid email or password"

def test_login_fail_wrong_email(client):
    response = client.post("/login", 
        json={"email": "wrong@test.com", "password":"password123"})

    assert response.status_code == 401
    data = response.get_json()

    assert data["message"] == "Invalid email or password"

def test_login_missing_password(client,customer_user):
    response = client.post("/login", 
                           json = ({"email":"customer@test.com","password":""}))
    assert response.status_code == 400
    data = response.get_json()

    assert data["message"] == "missing password"

def test_login_missing_email(client,customer_user):
    response = client.post("/login", 
                           json = ({"email": "","password":"password123"}))
    assert response.status_code == 400
    data = response.get_json()

    assert data["message"] == "missing email"


def test_login_invalid_json(client):
    response = client.post("/login", 
                           data = "invalid_json", content_type = "application/json")
    assert response.status_code == 400

def test_login_empty_fields(client,customer_user):
    response = client.post("/login", 
                           json = ({"email":"", "password": ""}))
    assert response.status_code == 400

def test_login_nonexistent_user(client):
    response = client.post("/login", 
                           json={
    "email":"nobody@test.com",
    "password":"1234"
})
    assert response.status_code == 401














def test_register_missing_password(client,customer_user):
    response = client.post("/register", 
                           json = ({"username":"customer","email":"customer@test.com","password":""}))
    assert response.status_code == 400
    data = response.get_json()

    assert data["message"] == "missing password"

def test_register_missing_email(client,customer_user):
    response = client.post("/register", 
                           json = ({"username":"customer","email": "","password":"password123"}))
    assert response.status_code == 400
    data = response.get_json()

    assert data["message"] == "missing email"


def test_register_invalid_json(client):
    response = client.post("/register", 
                           data = "invalid_json", content_type = "application/json")
    assert response.status_code == 400

def test_register_empty_fields(client,customer_user):
    response = client.post("/register", 
                           json = ({"username":"customer","email":"", "password": ""}))
    assert response.status_code == 400

def test_register_existenting_email(client,customer_user):
    response = client.post("/register", 
                           json={"username":"new_customer",
    "email":"customer@test.com",
    "password":"password123"
})
    assert response.status_code == 400
    data = response.get_json()
    assert data["message"] == "email is already exists"




