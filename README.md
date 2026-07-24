# Taskflow Task Tracker

Taskflow is a small FastAPI and vanilla-JavaScript Kanban application built for the AUB AI-Assisted Coding mid-course project.

## Current baseline

The baseline reproduces the Task Tracker developed across Modules 1-3:

- strict Pydantic v2 task models;
- in-memory CRUD API;
- backend-enforced status transitions;
- pytest coverage and model verification;
- three-column Kanban board with priority sorting;
- drag-and-drop persistence and rollback;
- create/edit modal with client and server validation.

## Run locally

Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Start the API from the repository root:

```powershell
python -m uvicorn app.main:app --reload --port 8000
```

In a second terminal, start the frontend:

```powershell
python -m http.server 5500 --directory frontend
```

Open:

- Frontend: http://localhost:5500
- Swagger API documentation: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## Verify

```powershell
python -m tests.verify_a
python -m pytest tests -v
```

The project uses in-memory storage by design. Restarting the API clears tasks.
