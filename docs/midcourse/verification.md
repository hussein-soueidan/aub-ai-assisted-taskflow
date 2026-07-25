# Verification

## Environment and baseline

- Python used for the project virtual environment: 3.10.
- Baseline commit: `32606f1` (`build Module 1-3 task tracker baseline`).
- Feature checkpoint commit: `75bab32`.
- Focused refactor commit: `3d0f97a`.

The supplied `D:\AUB\Midterm` folder was empty, so the Module 1-3 Task Tracker baseline was recreated from the course notes before feature work began.

Baseline commands and results:

```text
> python -m tests.verify_a
8 PASS lines; 0 FAIL

> python -m pytest tests -q
20 passed
```

## Final automated results

```text
> python -m pytest tests -v
42 passed, 1 warning in 0.23s
```

The 42 tests include the original 20 baseline tests, 20 feature/extension tests,
and 2 facilitator-feedback regression tests. Covered areas include due-date
validation, overdue true/false filtering, tag normalization and limits, combined
queries, bulk partial failures, CRUD, status transitions, explicit null updates,
and delete behavior.

Frontend syntax check:

```text
> node -e "...new Function(extractedScript)..."
JavaScript syntax OK
```

The remaining warning is emitted by the installed Starlette `TestClient` compatibility shim and does not change test outcomes.

## Facilitator feedback regression

The first submission accepted explicit `null` values for `title` and `status`.
This could store an invalid task, and a later status update could fail with a
500 response when the transition rule tried to read the invalid status.

Root cause:

- `TaskUpdate` used `None` for both omitted fields and explicit JSON nulls.
- `model_copy(update=...)` did not revalidate the completed stored task.

Correction:

- Explicit nulls are rejected for `title`, `description`, `status`, `priority`,
  and `tags`; omitting those fields is still valid for a partial update.
- Intentionally nullable `assignee` and `due_date` fields can still be cleared.
- The storage layer now constructs and validates a complete `TaskResponse`
  before replacing stored state.

Regression evidence:

```text
tests/test_tasks.py::test_patch_null_title_returns_422_and_preserves_title PASSED
tests/test_tasks.py::test_patch_null_status_returns_422_without_corrupting_later_updates PASSED
```

The second test follows the rejected `status: null` request with a valid
`ToDo` to `InProgress` update and receives 200, proving stored state remains
usable. The complete suite then passed 42/42 tests.

## Manual Chrome checks

The backend ran on `localhost:8000` and the static frontend on `localhost:5500`.

| Check | Evidence | Result |
| --- | --- | --- |
| Empty board | To Do, In Progress, and Done all remained visible with count 0 | PASS |
| Create due/tag task | Created `Ship API review`, High priority, due 2026-07-20, tags `backend` and `urgent` | PASS |
| Card rendering | Card displayed title, description, priority, assignee, overdue label, and both chips | PASS |
| Priority sorting | A second Low-priority future task appeared below the High-priority task | PASS |
| Overdue filter | Selecting Overdue only returned one task and retained all three columns | PASS |
| Responsive visual hierarchy | Header, filter panel, board, empty states, and cards rendered without overlap at the active desktop viewport | PASS |

## Behavior contract before and after refactor

The refactor extracted repeated 404 construction to `_task_not_found()` without changing routes or response details.

| Contract item | Before refactor | After refactor |
| --- | --- | --- |
| Health endpoint returns 200 | PASS | PASS |
| Create validation and 201 response | PASS | PASS |
| Five CRUD routes retain status/body contracts | PASS | PASS |
| Status-transition matrix is unchanged | PASS | PASS |
| Due-date validation and overdue filter | PASS | PASS |
| Tag normalization and tag filter | PASS | PASS |
| Bulk update/delete partial failures | PASS | PASS |
| Frontend JavaScript parses and required board/modal/filter controls remain present | PASS | PASS |

Evidence: the then-current 40/40 pytest tests passed immediately before and
after the refactor; the JavaScript syntax check passed after the refactor.

## Break Test 1 - Tag normalization

Protected test:

```text
tests/test_midcourse_features.py::test_tags_are_trimmed_lowercased_and_deduplicated
```

Temporary source break:

```python
cleaned = value.strip()  # removed .lower()
```

Observed failure:

```text
AssertionError:
['Backend', 'Urgent', 'backend'] != ['backend', 'urgent']
1 failed
```

The failure proves the test protects both lowercase normalization and case-insensitive deduplication. After restoring `.lower()`, the targeted test passed.

## Break Test 2 - Overdue detection

Protected test:

```text
tests/test_midcourse_features.py::test_overdue_filter_returns_only_unfinished_past_due_tasks
```

Temporary source break:

```python
task.due_date <= date.max  # replaced task.due_date < today
```

Observed failure:

```text
AssertionError: response contained one extra future task id
1 failed
```

The failure proves the test distinguishes genuinely overdue work from future
work. After restoring `< today`, the targeted test and the then-current
40-test suite passed.

## Debugging decisions

- The first full run failed on Python 3.10 because `datetime.UTC` is a Python 3.11 feature. The source was corrected to `timezone.utc`; this was a cause fix, not a test change.
- The first edit-modal payload included every field, including an unchanged status. Because same-to-same status transitions are intentionally rejected, the final frontend computes a diff and sends only changed fields.
- A Windows UI helper stopped when it could not prove Chrome's current URL. No safety bypass was attempted; browser validation continued only through already-authorized local checks.
