from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
import uvicorn

from . import models, schemas, crud
from .database import engine, SessionLocal

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskTrack - Task Management System")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db)
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db)
    completed_tasks = [task for task in tasks if task.status == "completed"]
    in_progress_tasks = [task for task in tasks if task.status == "in_progress"]
    new_tasks = [task for task in tasks if task.status == "new"]
    
    return templates.TemplateResponse(
        "dashboard.html", 
        {
            "request": request, 
            "tasks": tasks,
            "completed_count": len(completed_tasks),
            "in_progress_count": len(in_progress_tasks),
            "new_count": len(new_tasks)
        }
    )

@app.get("/tasks", response_class=HTMLResponse)
async def tasks_page(
    request: Request, 
    status: Optional[str] = None,
    priority: Optional[str] = None,
    db: Session = Depends(get_db)
):
    tasks = crud.get_filtered_tasks(db, status=status, priority=priority)
    return templates.TemplateResponse("tasks.html", {"request": request, "tasks": tasks})

@app.get("/tasks/create", response_class=HTMLResponse)
async def create_task_form(request: Request):
    return templates.TemplateResponse("create_task.html", {"request": request})

@app.post("/tasks/create")
async def create_task(
    title: str = Form(...),
    description: str = Form(...),
    due_date: str = Form(...),
    priority: str = Form(...),
    assignee: str = Form(...),
    db: Session = Depends(get_db)
):
    task_data = schemas.TaskCreate(
        title=title,
        description=description,
        due_date=due_date,
        priority=priority,
        assignee=assignee
    )
    crud.create_task(db, task_data)
    return RedirectResponse(url="/tasks", status_code=303)

@app.get("/tasks/{task_id}", response_class=HTMLResponse)
async def get_task(task_id: int, request: Request, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return templates.TemplateResponse("task_detail.html", {"request": request, "task": task})

@app.get("/tasks/{task_id}/edit", response_class=HTMLResponse)
async def edit_task_form(task_id: int, request: Request, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return templates.TemplateResponse("edit_task.html", {"request": request, "task": task})

@app.post("/tasks/{task_id}/edit")
async def edit_task(
    task_id: int,
    title: str = Form(...),
    description: str = Form(...),
    due_date: str = Form(...),
    priority: str = Form(...),
    status: str = Form(...),
    assignee: str = Form(...),
    db: Session = Depends(get_db)
):
    task_data = schemas.TaskUpdate(
        title=title,
        description=description,
        due_date=due_date,
        priority=priority,
        status=status,
        assignee=assignee
    )
    task = crud.update_task(db, task_id, task_data)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return RedirectResponse(url=f"/tasks/{task_id}", status_code=303)

@app.post("/tasks/{task_id}/delete")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    success = crud.delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return RedirectResponse(url="/tasks", status_code=303)

# API endpoints for AJAX requests
@app.get("/api/tasks")
async def get_tasks_api(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    db: Session = Depends(get_db)
):
    tasks = crud.get_filtered_tasks(db, status=status, priority=priority)
    return tasks

@app.get("/api/dashboard/stats")
async def get_dashboard_stats(
    time_period: str = "week",
    db: Session = Depends(get_db)
):
    # In a real app, we would filter by time period
    # For this demo, we'll return mock data
    tasks = crud.get_tasks(db)
    completed_tasks = [task for task in tasks if task.status == "completed"]
    in_progress_tasks = [task for task in tasks if task.status == "in_progress"]
    new_tasks = [task for task in tasks if task.status == "new"]
    
    # Mock data for charts
    if time_period == "day":
        labels = ["Morning", "Afternoon", "Evening"]
        completed_data = [2, 3, 1]
        in_progress_data = [3, 2, 4]
        new_data = [1, 2, 1]
    elif time_period == "week":
        labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        completed_data = [2, 3, 1, 4, 2, 0, 1]
        in_progress_data = [3, 2, 4, 1, 3, 1, 0]
        new_data = [1, 2, 1, 3, 2, 0, 1]
    else:  # month
        labels = ["Week 1", "Week 2", "Week 3", "Week 4"]
        completed_data = [7, 9, 6, 8]
        in_progress_data = [5, 7, 8, 4]
        new_data = [3, 5, 4, 6]
    
    return {
        "summary": {
            "completed": len(completed_tasks),
            "in_progress": len(in_progress_tasks),
            "new": len(new_tasks),
            "total": len(tasks)
        },
        "chart_data": {
            "labels": labels,
            "datasets": [
                {
                    "label": "Completed",
                    "data": completed_data
                },
                {
                    "label": "In Progress",
                    "data": in_progress_data
                },
                {
                    "label": "New",
                    "data": new_data
                }
            ]
        }
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 