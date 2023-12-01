from config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# database_name = settings.database_name
database_name = "test_db.db"
db_url = f"sqlite:///./{database_name}"

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
