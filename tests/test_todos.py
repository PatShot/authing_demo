import pytest


def create_new_task(auth_client):
    res = auth_client(
        "/todo/create", json= {
            "task_name": "this",
            "description": "something",
            "due_date": "2024-01-01",
            "priority": 4,
            "status": "STARTED"
        }
    )
    assert res.status_code == 201

# Get tasks
@pytest.mark.skip(reason="Issues with database fixtures.")
def test_get_tasks(auth_client,test_user, test_todos):
    res = auth_client.get("/todos/get")
    
    assert res.status_code == 200
    assert len(res.json()) == len(test_todos)
    