import pytest

from fastapi.testclient import TestClient
from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app, get_db
from app.database import Base
from app.models import Task

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def sample_task():
    return {
        "title": "Test Task",
        "description": "Test Description",
        "due_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "priority": "high",
        "assignee": "test_user"
    }

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_create_task(sample_task):
    response = client.post("/tasks/create", data=sample_task, follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/tasks"

    # Verify task was created
    response = client.get("/tasks")
    assert response.status_code == 200
    assert sample_task["title"] in response.text
    assert sample_task["description"] in response.text

def test_get_task_detail():
    # First create a task
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "due_date": "2024-12-31",
        "priority": "high",
        "assignee": "test_user"
    }
    client.post("/tasks/create", data=task_data)
    
    # Get the task (assuming it's the first task with ID 1)
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert task_data["title"] in response.text
    assert task_data["description"] in response.text

def test_edit_task():
    # First create a task
    task_data = {
        "title": "Original Title",
        "description": "Original Description",
        "due_date": "2024-12-31",
        "priority": "high",
        "assignee": "test_user"
    }
    client.post("/tasks/create", data=task_data)
    
    # Edit the task
    updated_data = {
        "title": "Updated Title",
        "description": "Updated Description",
        "due_date": "2024-12-31",
        "priority": "low",
        "status": "in_progress",
        "assignee": "new_user"
    }
    response = client.post("/tasks/1/edit", data=updated_data, follow_redirects=False)
    assert response.status_code == 303
    
    # Verify the changes
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert updated_data["title"] in response.text
    assert updated_data["description"] in response.text

def test_delete_task():
    # First create a task
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "due_date": "2024-12-31",
        "priority": "high",
        "assignee": "test_user"
    }
    client.post("/tasks/create", data=task_data)
    
    # Delete the task
    response = client.post("/tasks/1/delete", follow_redirects=False)
    assert response.status_code == 303
    
    # Verify task was deleted
    response = client.get("/tasks/1")
    assert response.status_code == 404

def test_get_filtered_tasks():
    # Create tasks with different statuses and priorities
    tasks = [
        {
            "title": "Task 1",
            "description": "High priority, new",
            "due_date": "2024-12-31",
            "priority": "high",
            "assignee": "user1"
        },
        {
            "title": "Task 2",
            "description": "Low priority, completed",
            "due_date": "2024-12-31",
            "priority": "low",
            "assignee": "user2"
        }
    ]
    
    for task in tasks:
        client.post("/tasks/create", data=task)
    
    # Test priority filter
    response = client.get("/api/tasks?priority=high")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["priority"] == "high"

def test_get_dashboard_stats():
    response = client.get("/api/dashboard/stats?time_period=week")
    assert response.status_code == 200
    data = response.json()
    
    # Check structure of response
    assert "summary" in data
    assert "chart_data" in data
    assert "labels" in data["chart_data"]
    assert "datasets" in data["chart_data"]
    
    # Check summary fields
    summary = data["summary"]
    assert all(key in summary for key in ["completed", "in_progress", "new", "total"])

def test_invalid_task_id():
    response = client.get("/tasks/999")
    assert response.status_code == 404 