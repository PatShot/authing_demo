from fastapi import APIRouter, status, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from app.database import schemas, models
from app.database.database import get_db
from app.utils import passutils, oauth2
from datetime import datetime

router = APIRouter(
    prefix="/todo",
    tags=['TaskItems']
)

# Helper functions for datetime parsing
def is_datetime_like(s):
    try:
        datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False

def convert_to_datetime(input_str):
    if is_datetime_like(input_str):
        return datetime.strptime(input_str, "%Y-%m-%d %H:%M:%S")
    else:
        try:
            return datetime.strptime(input_str, "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0)
        except ValueError:
            # Default assumption. Perhaps should raise Error instead?
            # Raising Error instead.
            # return datetime.now()+timedelta(hours=6)
            raise ValueError

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_task_item(
        task: schemas.TaskItem,
        db: Session = Depends(get_db),
        current_user = Depends(oauth2.get_curr_user)
    ):
    """
    Args
    ---
    TaskItem: 
        task_name: str
        description: str
        due_date: datetime, or date in YYYY-MM-DD format
        priority: int
        status: str, PENDING, STARTED, ON_HOLD, COMPLETED enum
    """
    try:
        task_due = convert_to_datetime(task.due_date)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)

    print(task_due, type(task_due))
    new_task = models.ToDoTask(
        user_id=current_user.id,
        task_name=task.task_name,
        description=task.description,
        due_date=task_due,
        priority=task.priority,
        status=task.status
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)


@router.get("/", status_code=status.HTTP_200_OK)
def get_task_items(
    db: Session = Depends(get_db),
    current_user = Depends(oauth2.get_curr_user)
    ):
    tasks = db.query(
        models.ToDoTask
    ).filter(
        models.ToDoTask.user_id == current_user.id
    ).all()

    results = {str(i):task for i, task in enumerate(tasks)}
    return results


