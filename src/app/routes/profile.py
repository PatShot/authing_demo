from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import schemas, models
from app.database.database import get_db
from app.utils import passutils, oauth2

router = APIRouter(
    prefix="/profiles",
    tags=['Profiles']
)

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_profile(
        profile_in: schemas.ProfileIn, 
        db: Session = Depends(get_db), 
        current_user = Depends(oauth2.get_curr_user)
    ):
    profile = profile_in.model_dump()
    print(profile)
    new_profile = models.Profile(
        user_id=current_user.id,
        name=profile["name"],
        display_handle=profile["display_handle"]
    ) 
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile

@router.get("/", response_model=schemas.ProfileOut)
def get_profile(db: Session = Depends(get_db), current_user  = Depends(oauth2.get_curr_user)):
    results = db.query(models.Profile, models.User).join(
        models.Profile, models.Profile.user_id == models.User.id
    ).filter(
        models.Profile.user_id == current_user.id
    ).first()

    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    profile_out = {}
    for profile, user in results:
        profile_out["user_id"] = profile.user_id
        profile_out["name"] = profile.name
        profile_out["username"] = user.username
        profile_out["email"] = user.email
        profile_out["display_handle"] = profile.display_handle
        profile_out["created_at"] = profile.created_at

    return schemas.ProfileOut(**profile_out)
