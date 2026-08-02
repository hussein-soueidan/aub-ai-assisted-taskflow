# Taskflow Task Tracker

Taskflow is a FastAPI and vanilla-JavaScript Kanban application for the AUB
AI-Assisted Coding course project. The release-readiness submission is on
`final-project`.

## Submission

- Public repository: https://github.com/hussein-soueidan/aub-ai-assisted-taskflow
- Final submitted branch: https://github.com/hussein-soueidan/aub-ai-assisted-taskflow/tree/final-project
- Preserved mid-course branch: https://github.com/hussein-soueidan/aub-ai-assisted-taskflow/tree/mid-course-project

## Final Project

Branch reviewed: `final-project`

### What this submission demonstrates

- The existing Task Tracker still runs inside the intended course scope.
- CI runs the pytest suite on push and pull request.
- The Docker image builds and runs with `/health` returning 200 and the process
  owned by a non-root `app` user.
- AI review, security, governance, and ownership evidence is in `docs/`.
- No new product feature or final-project edit to `app/`/`frontend/` was made.

### How to run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

In a second terminal:

```powershell
python -m http.server 5500 --directory frontend
```

Open `http://localhost:5500`; API docs are at `http://localhost:8000/docs`.

### How to run tests

```powershell
python -m tests.verify_a
python -m pytest tests -v
```

The final baseline is 8 model PASS checks and 42 passing pytest tests.

### How to run with Docker

The image serves the backend API; serve `frontend/` separately as shown above.

```text
docker build --pull -t taskflow:final .
docker run --rm -d --name taskflow-final -p 8000:8000 taskflow:final
curl --fail http://127.0.0.1:8000/health
docker exec taskflow-final whoami
docker stop taskflow-final
```

The health call should return JSON with `"status":"ok"`; `whoami` should
return `app`.

### Final evidence files

- [Release evidence](docs/release-evidence.md)
- [Final AI review and ownership](docs/final-ai-review.md)
- [Personal AI playbook](docs/ai-playbook.md)
- [Security review](docs/security-review.md)
- [Governance worksheet](docs/governance-worksheet.md)
- [Architecture](docs/architecture.md)
- [Release-engineering decision](docs/decisions/release-engineering.md)
- [Reusable release-safety checklist](docs/checklists/release-safety.md)

### AI assistance summary

AI helped draft and review CI, Docker, documentation, security findings, and
release evidence. I verified the work with the full test suite, a live `/health`
request, browser checks, diff/config inspection, tracked-secret scans, and the
CI container smoke test. I rejected advice to skip the container runtime check
and corrected any claim that Docker was verified locally, because this Windows
environment does not have Docker installed.

## What is included

The Module 1-3 baseline provides:

- strict Pydantic v2 models and an in-memory storage layer;
- five CRUD routes plus backend-enforced status transitions;
- a responsive three-column board with priority ordering;
- drag-and-drop persistence with rollback on rejected transitions;
- create/edit modal validation and API error handling.

The two selected mid-course features are:

- **Due dates and overdue filtering** - optional ISO dates, due/overdue card indicators, update/clear support, and a backend overdue filter that excludes completed tasks.
- **Tags and labels** - up to five normalized tags, card chips, update support, validation, and case-insensitive tag filtering.

All optional extensions from the brief are also implemented:

- **Bulk operations** with multi-select, batch status updates, batch deletion, and per-task partial-failure reporting.
- **Saved views** stored in browser `localStorage`, covering search, status, priority, tag, and overdue filters.
- **Frontend polish** with persistent light/dark themes, responsive layout, focus styling, reduced-motion support, and subtle card/modal animation.

Combined text search and filters were added to support useful saved views.

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

In a second terminal, serve the static frontend:

```powershell
python -m http.server 5500 --directory frontend
```

Open:

- Frontend: http://localhost:5500
- Swagger API documentation: http://localhost:8000/docs
- Health check: http://localhost:8000/health

The API allows the local origins used above. If a different frontend port is used, add only that local origin to the CORS list in `app/main.py`.

## API highlights

`GET /tasks` accepts combinable query parameters:

| Parameter | Example | Behavior |
| --- | --- | --- |
| `status` | `Done` | Exact enum match |
| `priority` | `High` | Exact enum match |
| `tag` | `backend` | Case-insensitive normalized tag |
| `overdue` | `true` | Past due and not Done |
| `search` | `release` | Case-insensitive title/description search |

Bulk endpoints:

- `PATCH /tasks/bulk` with `{ "task_ids": [...], "changes": {...} }`
- `POST /tasks/bulk-delete` with `{ "task_ids": [...] }`

Both return successful items and structured per-task errors rather than hiding partial failures.

## Verify

```powershell
python -m tests.verify_a
python -m pytest tests -v
```

The final suite contains 42 tests: the original 20 baseline tests, 20 feature and
extension tests, and 2 facilitator-feedback regression tests for explicit null
task updates. JavaScript syntax can be checked with Node:

```powershell
node -e "const fs=require('fs');const h=fs.readFileSync('frontend/index.html','utf8');new Function(h.match(/<script>([\s\S]*)<\/script>/)[1]);console.log('JavaScript syntax OK')"
```

## Project evidence

- [User stories](docs/midcourse/user-stories.md)
- [Mini ADR](docs/midcourse/mini-adr.md)
- [Prompt log](docs/midcourse/prompt-log.md)
- [Verification and break tests](docs/midcourse/verification.md)
- [Reflection](docs/midcourse/reflection.md)
- [Optional extensions](docs/midcourse/optional-extensions.md)
- [API summary](docs/midcourse/api-summary.md)
- [Submission checklist](docs/midcourse/submission.md)

## Data and scope

Storage is intentionally in memory to match the course architecture. Restarting
the API clears tasks. The repository contains no authentication, credentials,
private data, production database, deployment workflow, or claim of production
readiness. Docker packages the backend API only.
