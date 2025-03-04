# TaskTrack - Task Management System

TaskTrack is a web application for managing tasks and monitoring productivity. It allows users to create, track, and analyze tasks through an interactive dashboard.

## Features

- Complete task management (CRUD operations)
- Interactive dashboard with charts and statistics
- Filtering and sorting of tasks
- Responsive design for desktop and mobile devices

## Technology Stack

- Backend: Python 3.11+ with FastAPI
- Database: SQLite
- Frontend: Jinja2 templates, HTML, CSS, JavaScript
- Charts: Chart.js

## Installation and Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/tasktrack.git
   cd tasktrack

   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   ```

3. Install the dependencies:
   ```
   pip install -r requirements.txt

   ```

4. Run the application:
   ```
   python -m uvicorn app.main:app --reload

   ```

5. Open your browser and navigate to:
   ```
   http://localhost:8000

   ```

Testing:

```
pytest app/tests/test_main.py -v

```

## Project Structure

- `app/main.py`: Main application file with FastAPI routes
- `app/models.py`: SQLAlchemy database models
- `app/schemas.py`: Pydantic schemas for data validation
- `app/crud.py`: CRUD operations for database interaction
- `app/templates/`: Jinja2 HTML templates
- `app/static/`: Static files (CSS, JavaScript)
- `app/tests/`: Test suite

## API Documentation

### Task Management Endpoints

#### Create Task
- **URL**: `/tasks/create`
- **Method**: `POST`
- **Form Parameters**:
  - `title` (string, required): Task title
  - `description` (string, required): Task description
  - `due_date` (string, required): Due date in YYYY-MM-DD format
  - `priority` (string, required): Task priority (high/medium/low)
  - `assignee` (string, required): Task assignee
- **Response**: Redirects to `/tasks` on success
- **Status Codes**:
  - `303`: Successful creation
  - `422`: Validation error

#### Get Task List
- **URL**: `/tasks`
- **Method**: `GET`
- **Query Parameters**:
  - `status` (string, optional): Filter by status (new/in_progress/completed)
  - `priority` (string, optional): Filter by priority (high/medium/low)
- **Response**: HTML page with task list
- **Status Code**: `200`

#### Get Task Detail
- **URL**: `/tasks/{task_id}`
- **Method**: `GET`
- **Parameters**:
  - `task_id` (integer): Task ID
- **Response**: HTML page with task details
- **Status Codes**:
  - `200`: Success
  - `404`: Task not found

#### Edit Task
- **URL**: `/tasks/{task_id}/edit`
- **Method**: `POST`
- **Parameters**:
  - `task_id` (integer): Task ID
- **Form Parameters**:
  - `title` (string, required): Updated task title
  - `description` (string, required): Updated description
  - `due_date` (string, required): Updated due date
  - `priority` (string, required): Updated priority
  - `status` (string, required): Updated status
  - `assignee` (string, required): Updated assignee
- **Response**: Redirects to `/tasks` on success
- **Status Codes**:
  - `303`: Successful update
  - `404`: Task not found
  - `422`: Validation error

#### Delete Task
- **URL**: `/tasks/{task_id}/delete`
- **Method**: `POST`
- **Parameters**:
  - `task_id` (integer): Task ID
- **Response**: Redirects to `/tasks` on success
- **Status Codes**:
  - `303`: Successful deletion
  - `404`: Task not found

### Dashboard API Endpoints

#### Get Dashboard Statistics
- **URL**: `/api/dashboard/stats`
- **Method**: `GET`
- **Query Parameters**:
  - `time_period` (string, required): Time period for statistics (day/week/month)
- **Response**: JSON with dashboard statistics
  ```json
  {
    "summary": {
      "total": 10,
      "completed": 3,
      "in_progress": 4,
      "new": 3
    },
    "chart_data": {
      "labels": ["Mon", "Tue", "Wed", "Thu", "Fri"],
      "datasets": [
        {
          "label": "Tasks Created",
          "data": [2, 3, 1, 4, 0]
        }
      ]
    }
  }
  ```
- **Status Code**: `200`

#### Get Filtered Tasks
- **URL**: `/api/tasks`
- **Method**: `GET`
- **Query Parameters**:
  - `status` (string, optional): Filter by status
  - `priority` (string, optional): Filter by priority
  - `assignee` (string, optional): Filter by assignee
- **Response**: JSON array of tasks
  ```json
  [
    {
      "id": 1,
      "title": "Example Task",
      "description": "Task description",
      "due_date": "2024-12-31",
      "priority": "high",
      "status": "new",
      "assignee": "john.doe"
    }
  ]
  ```
- **Status Code**: `200`

## Error Handling

The API uses standard HTTP status codes:
- `200`: Successful request
- `303`: Successful redirect after POST
- `404`: Resource not found
- `422`: Validation error
- `500`: Server error

Error responses include a detail message and are rendered using appropriate error templates.