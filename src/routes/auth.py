from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, status, Depends
from src.database.database import get_db
import src.database.schemas as schemas
import src.database.models as models


router = APIRouter(tags=["Authenticate"])

@router.post("/login", response_model=schemas.Token)
def login(cred: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == cred.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid Credentials"
        )

    access_token = {"token_dummy": "xyz"}

    return {"access_token": access_token, "token_type": "bearer"}