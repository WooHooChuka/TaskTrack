from pydantic import BaseModel
from typing import Optional, List, Dict, Any
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

class TaskFilter(BaseModel):
    status: Optional[str] = None  # 'new', 'in_progress', 'completed'
    priority: Optional[str] = None  # 'high', 'medium', 'low'

class ChartData(BaseModel):
    labels: List[str]
    datasets: List[Dict[str, Any]]

class DashboardSummary(BaseModel):
    total: int
    completed: int
    in_progress: int
    new: int

class DashboardStats(BaseModel):
    summary: DashboardSummary
    chart_data: ChartData 