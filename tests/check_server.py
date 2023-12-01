import requests
from requests.exceptions import ConnectionError 

try:
    print(requests.get("http://127.0.0.1:8000/").json())
except ConnectionError:
    print("Connection has Error. Is server running?")

# Create new user
print(requests.post(
    "http://127.0.0.1:8000/users/create",
    json={"email": "janedoe@testmail.com", "password": "pass123"}
).json())
