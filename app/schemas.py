from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: str
    due_date: str
    priority: str
    assignee: str

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    status: str

class Task(TaskBase):
    id: int
    created_at: datetime
    status: str

    class Config:
        orm_mode = True 