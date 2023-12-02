from fastapi import APIRouter, status, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from src.database import schemas, models
from src.database.database import get_db
from src.utils import passutils, oauth2
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


@router.get("/get", status_code=status.HTTP_200_OK)
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

@router.delete("/delete/{idx}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_items(
    idx: int,
    db: Session = Depends(get_db),
    current_user = Depends(oauth2.get_curr_user)
    ):
    """
    Delete specific task with task_id idx for current
    logged in user
    """

    task_query = db.query(
        models.ToDoTask
    ).filter(
        models.ToDoTask.task_id == idx
    )

    task_del = task_query.first()
    if task_del == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if task_del.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    task_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{idx}", response_model=schemas.TaskItem)
def update_task_item(
    idx: int,
    task_updated: schemas.TaskItem,
    db: Session = Depends(get_db),
    current_user = Depends(oauth2.get_curr_user)
    ):
    """
    Update a specific task.
    Args:
    ---
    idx: id of task
    task_update: input from body with updated fields from
        frontend
    """
    task_query = db.query(
        models.ToDoTask
    ).filter(
        models.ToDoTask.task_id == idx
    )

    task = task_query.first()
    if task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if task.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    task_query.update(task_updated.model_dump(), synchronize_session=False)
    db.commit()
    
    check_task =task_query.first()
    if check_task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    task_out = {
        "task_name": check_task.task_name,
        "description": check_task.description,
        "due_date": str(check_task.due_date),
        "priority": check_task.priority,
        "status": check_task.status
    }
    return schemas.TaskItem(**task_out)
