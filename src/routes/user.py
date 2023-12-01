from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
import src.database.schemas as schemas
import src.database.models as models
from src.database.database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
