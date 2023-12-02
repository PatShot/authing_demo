from fastapi import APIRouter, status, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from src.database import schemas, models
from src.database.database import get_db
from src.utils import passutils, oauth2

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

    profile_out = {
        "name" : results.Profile.name,
        "user_id" : results.Profile.user_id,
        "username" : results.User.username,
        "email" : results.User.email,
        "display_handle" : results.Profile.display_handle,
        "created_at" : results.Profile.created_at
    }

    return schemas.ProfileOut(**profile_out)

@router.delete("/delete/{idx}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(idx: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_curr_user)):
    prof_query = db.query(models.Profile).filter(models.Profile.id == idx)
    profile = prof_query.first()
    if profile == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if profile.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    prof_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{idx}", response_model=schemas.ProfileShortOut)
def update_profile(
        idx: int,
        updated_profile: schemas.ProfileIn, 
        db:Session = Depends(get_db),
        current_user = Depends(oauth2.get_curr_user)
    ):
    prof_query = db.query(models.Profile).filter(models.Profile.id == idx)
    profile = prof_query.first()
    if profile == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if profile.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    new_profile = {
        "user_id": profile.user_id,
        "name": updated_profile.name,
        "display_handle": updated_profile.display_handle
    }
    # print(new_profile)
    
    prof_query.update(new_profile, synchronize_session=False)
    db.commit()

    results = prof_query.first()
    if results == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    profile_out = {
        "id": results.id,
        "name" : results.name,
        "user_id" : results.user_id,
        "display_handle" : results.display_handle,
        "created_at" : results.created_at
    }

    return schemas.ProfileShortOut(**profile_out)
