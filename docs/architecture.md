# Taskflow Architecture

## System overview

Taskflow is a local learning application with a FastAPI JSON API and a single
vanilla-JavaScript Kanban page. It intentionally uses in-memory storage and no
authentication or production database. The final-project release layer adds
CI, a non-root backend container, and evidence documents without changing the
product.

## Components and request flow

1. `frontend/index.html` sends JSON requests to the API and renders the three
   status columns, modal forms, filters, bulk controls, presets, and theme.
2. `app/main.py` maps HTTP routes to Pydantic request/response types and applies
   status-transition rules before storage updates.
3. `app/models.py` validates titles, enums, dates, tags, bulk request shape, and
   explicit-null update behavior.
4. `app/business_rules.py` owns the permitted status-transition matrix.
5. `app/storage.py` creates UUID/timestamps, stores `TaskResponse` objects in a
   process-wide dictionary, applies filters, and revalidates completed updates.
6. `tests/` exercises the API through FastAPI's TestClient; browser checks cover
   the visible board/modal flow.

## Release and verification layer

- `.github/workflows/ci.yml` runs the 42-test suite on Python 3.11 and separately
  builds/runs the container, calls `/health`, and checks the non-root user.
- `Dockerfile` uses a builder venv and a slim runtime that copies only runtime
  dependencies and `app/`.
- `.dockerignore` keeps secrets, local environments, evidence, and unrelated
  files outside the build context.
- `AGENTS.md` tells future repo-aware assistants to read first, protect product
  code, cite evidence, and keep final work docs-first.

## Known limits

Restarting the API loses tasks. The Docker image serves the backend API, while
the frontend remains a separately served static page. There is no authentication,
rate limiting, production persistence, deployment workflow, or claim of
production readiness.

## Context-engineering rule

I used targeted context (`main.py`, `models.py`, `storage.py`, business rules,
tests, and the frontend) for correctness/security claims because it limits
invention. I used structured context (`AGENTS.md` plus the repository map) for
onboarding/release documentation because that task needs broader coverage.
