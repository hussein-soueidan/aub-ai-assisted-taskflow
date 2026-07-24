# API Summary

## Models

### TaskCreate

- Required: `title`
- Optional/defaulted: `description`, `status`, `priority`, `assignee`, `due_date`, `tags`
- Unknown fields are rejected.

### TaskUpdate

All editable fields are optional. `id`, `created_at`, and `updated_at` are rejected as client input.

### TaskResponse

Includes all task fields plus server-generated `id`, `created_at`, and `updated_at`.

## Enums and rules

- Status: `ToDo`, `InProgress`, `Done`
- Priority: `Low`, `Medium`, `High`
- Valid transitions:
  - ToDo -> InProgress
  - InProgress -> Done
  - Done -> InProgress
- Same-to-same and all other transitions return 422.
- A title is trimmed, required, and limited to 200 characters.
- Tags are lowercased, deduplicated, nonblank, limited to five, and limited to 24 characters each.

## Routes

| Method | Route | Success |
| --- | --- | --- |
| GET | `/health` | 200 |
| POST | `/tasks` | 201 |
| GET | `/tasks` | 200 |
| GET | `/tasks/{task_id}` | 200 |
| PATCH | `/tasks/{task_id}` | 200 |
| DELETE | `/tasks/{task_id}` | 204, empty body |
| PATCH | `/tasks/bulk` | 200 with updated items and errors |
| POST | `/tasks/bulk-delete` | 200 with deleted ids and errors |

Missing task ids return 404. Request/model validation and invalid transitions return 422.

## Query behavior

`GET /tasks` accepts `status`, legacy-compatible `status_filter`, `priority`, `tag`, `overdue`, and `search`. Supplied filters combine with AND semantics. Empty results return `[]`, never 404.

## Verification

- Model verification: 8 PASS checks.
- Baseline suite: 20 passing tests.
- Final suite: 40 passing tests.
- Break Test proof: tag normalization and overdue detection each failed when its production rule was intentionally broken, then passed after restoration.
