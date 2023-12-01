from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import models, database, schemas
from config import settings
from jose import jwt, JWTError

auth_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
EXPIRE_TIME = settings.jwt_expire_minutes
ALGORITHM = settings.algorithm

def create_access_token(data: dict):
    encoding_data = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_TIME)
    encoding_data.update({"exp": expire})

    encoded_jwt = jwt.encode(encoding_data, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, creds_err):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = decoded.get("user_id")
        if id is None:
            raise creds_err
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise creds_err

    return token_data


def get_curr_user(token:str = Depends(auth_scheme), db: Session = Depends(database.get_db)):
    creds_err = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = f"Credentials Invalid",
        headers = {"WWW-Authenticate": "Bearer"}
    )

    verified_token = verify_access_token(token, creds_err)

    user = db.query(models.User).filter(models.User.id == verified_token.id).first()
    return user
