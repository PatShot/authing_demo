from src.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

print(settings["database_username"])
# database_name = settings.database_name
database_name = "test_db"
# db_url = f"sqlite:///./{database_name}"
db_url = f'postgresql://{settings["database_username"]}:{settings["database_password"]}@{settings["database_hostname"]}:{settings["database_port"]}/{settings["database_name"]}'

engine = create_engine(db_url)
session_factory = sessionmaker(autoflush=False, autocommit=False, bind=engine)

SessionLocal = scoped_session(session_factory)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
