# Release Evidence

## Baseline

- Branch: `final-project`
- Date: 2026-08-02
- Local environment: Windows, Python 3.10.11
- API command: `python -m uvicorn app.main:app --host 127.0.0.1 --port 8000`
- `/health` result: HTTP 200 with
  `{"status":"ok","timestamp":"2026-08-02T11:57:13.063859+00:00"}`.
- Frontend command: `python -m http.server 5500 --bind 127.0.0.1 --directory frontend`
- Frontend check: HTTP 200; the To Do, In Progress, and Done columns rendered.
  I opened the New task modal, created `Final baseline check`, and opened its
  Edit task modal. No final-project code change was needed.
- Test command: `python -m pytest tests -v`
- Test result: 42 passed, 1 non-fatal Starlette compatibility warning in 0.32s.
- Model verification: `python -m tests.verify_a` returned 8 PASS lines.

## Scope control

- Final work is isolated on `final-project` from mid-course commit `4301acd`.
- No product feature was added.
- `app/` and `frontend/` were not changed during final-project work.
- The two untracked LMS/source files already present locally were not added to
  Git: `Midtern.pdf` and `Hussein Soueidan - Midterm Project.txt`.

## CI evidence

- Workflow: `.github/workflows/ci.yml`
- First published run (red evidence):
  [run 30747467470](https://github.com/hussein-soueidan/aub-ai-assisted-taskflow/actions/runs/30747467470).
  Pytest passed, while the Docker build correctly failed because the broad
  `*.txt` ignore rule also removed `requirements.txt` from the build context.
- Correction: added the narrow `!requirements.txt` exception; no application
  code or test expectation was changed.
- Verified green run:
  [run 30747512895](https://github.com/hussein-soueidan/aub-ai-assisted-taskflow/actions/runs/30747512895).
  Both `Pytest` and `Docker build and runtime smoke test` completed successfully.
- Workflow history:
  [CI runs](https://github.com/hussein-soueidan/aub-ai-assisted-taskflow/actions/workflows/ci.yml).
- Test command used by CI: `python -m pytest tests -v`
- Python version: explicitly `3.11`.
- Container job: builds the Dockerfile, starts the API, checks `/health`, and
  asserts `whoami` is `app`.
- Shortcut audit: no `continue-on-error`, no `|| true`, no skipped pytest, no
  exit-zero flag, no piped pytest output, and no deployment step.
- Workflow permissions are read-only (`contents: read`).

## Docker evidence

- Intended local build: `docker build --pull -t taskflow:final .`
- Intended local run:
  `docker run --rm -d --name taskflow-final -p 8000:8000 taskflow:final`
- Health check: `curl --fail http://127.0.0.1:8000/health`
- Non-root check: `docker exec taskflow-final whoami` must return `app`.
- Stop command: `docker stop taskflow-final`
- Local limitation: Docker is not installed on this workstation, so I do not
  claim a local container run. The CI `container-smoke` job performs the same
  build/run, HTTP 200, and non-root checks on GitHub's Ubuntu runner.
- Safety inspection: the runtime uses `python:3.11-slim`, runs as UID/GID 10001,
  copies only `/opt/venv` and `app/`, and has an explicit non-reload Uvicorn CMD.
- No-baked-secrets check: `.dockerignore` excludes `.env*`, `.git`, virtual
  environments, caches, logs, docs, tests, frontend, PDFs, and text files.

## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made, if any |
| --- | --- | --- | --- |
| `python -m pytest tests -v` is the full test command. | Executed from repo root on 2026-08-02. | PASS: 42 tests passed. | README keeps this exact command and count. |
| `GET /health` returns 200. | Running Uvicorn plus `Invoke-WebRequest`; `app/main.py`. | PASS: HTTP 200 and JSON status `ok`. | Recorded the actual response above. |
| The Kanban/create-edit flow is available at port 5500. | Running static server and in-app browser DOM/visual check. | PASS: three columns plus New/Edit task dialogs. | README keeps the static-server command. |
| Required update fields reject explicit null. | `tests/test_tasks.py` null regressions and full pytest run. | PASS: 422 and stored state remains valid. | Retained the facilitator-feedback note and tests. |
| DELETE returns an empty 204, not JSON. | `app/main.py` and `test_delete_existing_returns_204_no_body`. | PASS. | API wording remains 204/no body. |
| The container runs as non-root and serves `/health`. | Dockerfile inspection; successful CI runtime smoke [run 30747512895](https://github.com/hussein-soueidan/aub-ai-assisted-taskflow/actions/runs/30747512895). | PASS: image built, `/health` succeeded, and `whoami` returned `app`. | Retain the honest note that Docker was unavailable locally. |
