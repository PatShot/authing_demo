import pytest

def test_server(client):
    res = client.get("/")
    print(res.json())
    assert res.json().get('message') == 'HelloWorld'

