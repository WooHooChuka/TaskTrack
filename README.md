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

## Project Structure

- `app/main.py`: Main application file with FastAPI routes
- `app/models.py`: SQLAlchemy database models
- `app/schemas.py`: Pydantic schemas for data validation
- `app/crud.py`: CRUD operations for database interaction
- `app/templates/`: Jinja2 HTML templates
- `app/static/`: Static files (CSS, JavaScript)

## API Documentation

The API documentation is available at: 