# Taskflow Repository Instructions

## Project and stack

Taskflow is the AUB AI-Assisted Coding course Task Tracker. It uses FastAPI,
Pydantic v2, Uvicorn, pytest/httpx, in-memory Python storage, and a dependency-
free HTML/CSS/JavaScript frontend. CI and Docker use Python 3.11; the recorded
Windows baseline also passes on Python 3.10.11.

Important paths:

- `app/main.py`: FastAPI routes and CORS configuration.
- `app/models.py`: request/response schemas and validation.
- `app/storage.py`: in-memory CRUD and filtering.
- `app/business_rules.py`: permitted status transitions.
- `frontend/index.html`: complete browser UI.
- `tests/`: API and feature regression tests.
- `docs/`: course evidence, decisions, reviews, and release notes.

## Commands from the repository root

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
python -m http.server 5500 --directory frontend
python -m tests.verify_a
python -m pytest tests -v
```

Container verification:

```text
docker build --pull -t taskflow:final .
docker run --rm -d --name taskflow-final -p 8000:8000 taskflow:final
curl --fail http://127.0.0.1:8000/health
docker exec taskflow-final whoami
docker stop taskflow-final
```

## Business rules to preserve

- Status values are `ToDo`, `InProgress`, and `Done`.
- Allowed transitions are `ToDo -> InProgress`, `InProgress -> Done`, and
  `Done -> InProgress`; same-status and skipped transitions return 422.
- Required update fields reject explicit JSON null; omitted fields remain
  unchanged. `assignee` and `due_date` are intentionally nullable.
- A task is overdue only when its due date is before today and it is not Done.
- Tags are trimmed, lowercased, deduplicated, limited to five, and limited to
  24 characters each.
- Storage is intentionally in memory. Do not introduce a database or imply
  persistence across API restarts.
- Bulk operations report per-task successes and failures rather than pretending
  to be transactional.

## Final-project guardrails

1. Read `README.md`, the relevant `docs/` evidence, and nearby source/tests
   before proposing a change. Cite real files; mark anything unseen as unknown.
2. Prefer read-only analysis and documentation changes. Do not change `app/` or
   `frontend/` unless a small bug/security correction is explicitly approved;
   explain any such change in `docs/final-ai-review.md` and add a regression test.
3. Keep one bounded task per review. Show and inspect the diff before accepting
   broad edits. Do not add authentication, comments, notifications, deployment,
   a production database, or unrelated UI work during finalization.
4. Run focused tests for the changed behavior, then the full suite. For CI or
   Docker changes, inspect the configuration and retain real runtime evidence.
5. Never add or expose `.env` values, tokens, credentials, private keys,
   production logs, or real personal/customer data. Do not run destructive Git
   or filesystem commands without explicit approval.
6. AI suggests and reviews; the developer grades the finding, verifies the
   command/output, rejects unsupported advice, and owns the final result.
