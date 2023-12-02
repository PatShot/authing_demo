import pytest
from src.config import settings
# import requests

# @pytest.fixture
# def valid_credentials():
#     return {"email": "user@example.com", "password": "string"}

# @pytest.fixture
# def get_valid_jwt(valid_credentials):
#     jwt_token = requests.post(
#         "http://127.0.0.1:8000/login",
#         json=valid_credentials
#     )
#     return jwt_token

# # def test_get_jwt(get_valid_jwt):
# #     jwt_token = get_valid_jwt
# #     assert jwt_token is not None

# port = "8000"
# BASE_URL = f"127.0.0.1:{port}/"
# API = BASE_URL+"{route}/{extension}"


from jose import jwt

# Create User
def test_createuser(client):
    res = client.post(
        "/users/create", json={
            "username":"tester",
            "email": "test@mail.com", 
            "password": "password123"
            }
    )
    new_user = res.json()
    assert new_user["email"] == "test@mail.com"
    assert new_user["username"] == "tester"
    assert res.status_code == 201

# Test Login for correct JWT return
def test_user_login(test_user, client):
    res = client.post(
        "/login", data = {
            "username": test_user['email'], "password": test_user["password"]
        }
    )
    login_res = res.json()
    payload = jwt.decode(login_res["access_token"], 
                         settings["secret_key"], algorithms=[settings["algorithm"]])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res['token_type'] == "bearer"
    assert res.status_code == 200


# Test Wrong Logins
@pytest.mark.parametrize("email, password, status_code", [
    ("notworking@mail.com", "sjkdnskj", 403),
    ("notworking@mail.com", "password123", 403),
    ("test@mail.com", "sdasas", 403),
    (None, "password123", 422),
    ("test@mail.com", None, 422)
])
def test_wrong_login(test_user, client, email, password, status_code):
    res = client.post("/login", data = {"username": email,"password": password})
    assert res.status_code == status_code