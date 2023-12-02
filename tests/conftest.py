import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.database.database import Base, get_db
from .settings import settings


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



