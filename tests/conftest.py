import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.database.database import Base, get_db
from src.database import models
from src.config import settings
from src.utils.oauth2 import create_access_token

print(settings)

# Test Database
TEST_DATABASE = f'postgresql://{settings["database_username"]}:{settings["database_password"]}@{settings["database_hostname"]}:{settings["database_port"]}/testbase'

engine = create_engine(TEST_DATABASE)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Pytest fixture scoped to function by default
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
        # give function as a closure to dependency_overrides
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {
        "username": "tester1",
        "email": "test@mail.com",
        "password": "password123"
    }
    res = client.post("/users/create", json = user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data["password"]
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def auth_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_profile(auth_client):
    res = auth_client.post(
        "/profiles/create", json = {
            "name": "Test Profile",
            "display_handle": "test.profile"
        }
    )

    assert res.status_code == 201

    new_profile = res.json()
    return new_profile


@pytest.fixture
def test_todos(test_user, session):
    data = [
        {'task_name': 'task_1', 'description': 'desc_1', 'due_date': '2024-01-01', 'priority': 3, 'status': 'PENDING', 'user_id': test_user["id"]},
        {'task_name': 'task_2', 'description': 'desc_2', 'due_date': '2024-01-02', 'priority': 4, 'status': 'STARTED', 'user_id': test_user["id"]},
        {'task_name': 'task_3', 'description': 'desc_3', 'due_date': '2024-01-03', 'priority': 4, 'status': 'PENDING', 'user_id': test_user["id"]},
        {'task_name': 'task_4', 'description': 'desc_4', 'due_date': '2024-01-04', 'priority': 0, 'status': 'ON-HOLD', 'user_id': test_user["id"]},
        {'task_name': 'task_5', 'description': 'desc_5', 'due_date': '2024-01-05', 'priority': 2, 'status': 'PENDING', 'user_id': test_user["id"]}
    ]
    def create_todo_model(task):
        return models.ToDoTask(**task)
    
    task_map = map(create_todo_model, data)
    todos = list(task_map)

    # Using Session add all -> all todos in database
    session.add_all(todos)
    session.commit()

    todos = session.query(models.ToDoTask).all()
    return todos