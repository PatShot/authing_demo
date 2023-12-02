import pytest

def test_server(client):
    print("Testing server ...")
    res = client.get("/")
    print(res.json())
