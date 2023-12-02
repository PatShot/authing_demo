from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str 


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class ForgotPass(BaseModel):
    email: EmailStr


class ResetPassToken(BaseModel):
    access_token: str
    token_type: str
    new_password: str


class ProfileIn(BaseModel):
    name: str
    display_handle: str
     

class ProfileCreate(ProfileIn):
    user_id: int


class ProfileOut(BaseModel):
    user_id: int 
    name: str
    username: str
    email: str
    display_handle: str
    created_at: datetime


class ProfileShortOut(BaseModel):
    id: int
    user_id: int
    name: str
    display_handle: str
    created_at: datetime
