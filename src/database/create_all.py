from src.database.database import engine
from src.database import models

def create_all_tables():
    print("Creating all tables...")
    models.Base.metadata.create_all(bind=engine)