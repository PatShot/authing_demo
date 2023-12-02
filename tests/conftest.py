import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.database.database import Base, get_db
from src.config import settings

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
    print("new_user")
    new_user['password'] = user_data["password"]
    return new_user

