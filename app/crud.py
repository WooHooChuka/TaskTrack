from sqlalchemy.orm import Session
from typing import Optional, List
from . import models, schemas

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()

def get_filtered_tasks(
    db: Session, 
    status: Optional[str] = None, 
    priority: Optional[str] = None,
    skip: int = 0, 
    limit: int = 100
):
    query = db.query(models.Task)
    
    if status:
        query = query.filter(models.Task.status == status)
    
    if priority:
        query = query.filter(models.Task.priority == priority)
    
    return query.offset(skip).limit(limit).all()

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        priority=task.priority,
        assignee=task.assignee,
        status="new"
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task: schemas.TaskUpdate):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        return None
    
    for key, value in task.dict().items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        return False
    
    db.delete(db_task)
    db.commit()
    return True 