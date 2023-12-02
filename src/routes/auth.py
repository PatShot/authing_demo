from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, status, Depends
from src.database.database import get_db
from src.database import schemas, models
from src.utils import passutils, oauth2


router = APIRouter(tags=["Authenticate"])

@router.post("/login", response_model=schemas.Token)
def login(cred: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)):
    """
    Args
    ---
    username: The email associated with the account
    passowrd: The password associated with the email
    Login user with a OAuth2 urlencoded post request. If valid, then return a JSON Web Token.
    If invalid, returns 403 Forbidden.
    """
    user = db.query(models.User).filter(
        models.User.email == cred.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid Credentials"
        )

    if not passutils.verify(cred.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid Credentials"
        )

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/forgot_password", status_code=status.HTTP_202_ACCEPTED)
def forgot_password(request: schemas.ForgotPass, db: Session = Depends(get_db)):
    """
    Args
    ----
    request: ForgotPass schema => email EmailStr
    
    Get an email from endpoint and check if such a user exists in database.
    Retunr a JWT with the current password of the user.
    This always returns a 202 Accepted to not allow malicious guesses.
    """
    result = db.query(models.User).filter(
        models.User.email == request.email
    ).first()

    if result:
        # One can also use uuid here.
        access_token = oauth2.create_access_token(data={"user_id": result.id, "pass": result.password}, mins=3)

    return {"access_token": access_token, "token_type": "reset_password"}


@router.post("/reset_password")
def reset_password(token: schemas.ResetPassToken, db:Session = Depends(get_db)):
    """
    Args
    ----
    token : str = JWT access token, with expiry within 3 mins.

    If valid then allow 
    """
    creds_err = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = f"Credentials Invalid",
        headers = {"WWW-Authenticate": "Bearer"}
    )
    if token.token_type == "reset_password":
        verified_token, token_pass = oauth2.verify_password_token(token.access_token, creds_err)

        user_query = db.query(models.User).filter(
            models.User.id == verified_token.id
        )

        user = user_query.first()

        if user == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        if user.password != token_pass:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
        hashed_newpassword = passutils.hash(token.new_password)
        updated_user = {
            "id": user.id,
            "email": user.email,
            "password": hashed_newpassword
        }

        user_query.update(updated_user, synchronize_session=False)
        db.commit()