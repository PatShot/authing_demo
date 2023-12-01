from app.database.database import engine
from app.database import models

def create_all_tables():
    print("Creating all tables...")
    models.Base.metadata.create_all(bind=engine)