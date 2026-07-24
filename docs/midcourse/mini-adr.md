# Mini ADR - Due Dates, Tags, and Optional Extensions

**Status:** Accepted  
**Date:** 2026-07-25  
**Branch:** `mid-course-project`

## Context

The Module 1-3 Task Tracker uses FastAPI, Pydantic v2, in-memory storage, and a dependency-free browser frontend. The mid-course brief requires two small end-to-end features and values review, test evidence, and constrained scope more than architectural ambition.

## Decision

I selected **due dates with overdue filtering** and **tags/labels** because both touch the model, storage/query behavior, API, modal, card rendering, and tests without replacing the course architecture.

`due_date` is an optional Pydantic `date`. The backend defines overdue as a non-Done task whose due date is before the current date. This keeps the query behavior authoritative, while the frontend mirrors the rule only for card presentation. Date-only semantics avoid an unnecessary timezone policy for a course task tracker.

`tags` is a list stored directly on `TaskCreate`, `TaskUpdate`, and `TaskResponse`. Tags are trimmed, lowercased, deduplicated, limited to five, and limited to 24 characters. The storage layer performs case-insensitive membership filtering. This is deliberately simpler than a normalized tag table because storage is already in memory.

All optional extensions were added in bounded forms:

- Bulk update and delete endpoints return successful items and structured per-task errors, allowing partial failures to remain visible.
- Saved views persist only filter definitions in browser `localStorage`; task data still belongs to the API.
- Light/dark themes and small CSS animations preserve the existing selectors and JavaScript behavior. Reduced-motion preferences are honored.

## Alternatives considered

- **Date-time plus timezone:** rejected because the brief specifies a due date and does not define time-of-day behavior.
- **Separate Tag model or database table:** rejected because it introduces persistence and relationship management outside the in-memory course design.
- **All-or-nothing bulk transactions:** rejected because there is no database transaction layer and the optional brief explicitly highlights partial-failure handling.
- **Server-persisted saved views:** rejected because it would require a settings model and persistence not central to Modules 1-3.
- **Frontend framework or animation library:** rejected to preserve the single-file vanilla frontend and keep diffs inspectable.

## Consequences

The design is easy to run and test locally and keeps all validation in Pydantic/FastAPI. In-memory storage remains the main limitation: tasks and saved backend state do not survive an API restart, while saved filter presets remain local to one browser. If the project grew, the first architecture revisit would be a persistent repository layer and migrations, not a change to the public task contract.
