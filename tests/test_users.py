import pytest
import requests

@pytest.fixture
def valid_credentials():
    return {"email": "user@example.com", "password": "string"}

@pytest.fixture
def get_valid_jwt(valid_credentials):
    jwt_token = requests.post(
        "http://127.0.0.1:8000/login",
        json=valid_credentials
    )
    return jwt_token

# def test_get_jwt(get_valid_jwt):
#     jwt_token = get_valid_jwt
#     assert jwt_token is not None

port = "8000"
BASE_URL = f"127.0.0.1:{port}/"
API = BASE_URL+"{route}/{extension}"


