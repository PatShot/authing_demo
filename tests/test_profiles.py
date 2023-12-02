import pytest

# Create New Profile
def test_create_new_profile(auth_client):
    res = auth_client.post(
        "/profiles/create", json = {
            "name": "Test Profile",
            "display_handle": "test.profile"
        }
    )

    new_profile = res.json()

    assert res.status_code == 201
    assert new_profile["name"] == "Test Profile"
    assert new_profile["user_id"] == 1 

# Get back profile
def test_get_profile(test_profile, auth_client):
    res = auth_client.get("/profiles/")
    assert res.status_code == 200

# Delete Profile
def test_delete_profile(test_profile, auth_client):
    res = auth_client.delete(
        "/profiles/delete/1"
    )
    assert res.status_code == 204

# PUT - Check if name and display_handle change
def test_alter_profile(test_profile, auth_client):
    alter_data = {
        "name": "Test2",
        "display_handle": "test.2"
    }
    res = auth_client.put("/profiles/1", json=alter_data)
    alter_prof = res.json()
    assert alter_prof["name"] == "Test2"
    assert res.status_code == 200