from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import schemas, models
from app.database.database import get_db
from app.utils import passutils

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = passutils.hash(user.password)
    user.password = hashed_password
    user_dict = user.model_dump()
    print(user_dict)
    new_user = models.User(email=user_dict["email"], password=user_dict["password"])
    db.add(new_user)
    db.commit()
    db.refresh(new_user)


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No User with id: {id}. They don't exist."
        )

    return user
