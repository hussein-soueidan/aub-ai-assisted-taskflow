# User Stories

The selected features are due dates with overdue filtering and tags/labels. Each story is intentionally small enough to implement and verify end-to-end.

## Feature 1 - Due dates and overdue filtering

### DD-1 - Add an optional due date

As a team member, I want to add an optional due date when creating a task so that I can see when the work is expected.

Acceptance criteria:

- A valid `YYYY-MM-DD` value is accepted and returned by `POST /tasks`.
- Omitting `due_date` is valid and returns `null`.
- A non-date value returns HTTP 422.
- The selected due date appears on the created card.

### DD-2 - See overdue work

As a team member, I want overdue tasks to be visually distinct so that late work is easy to notice.

Acceptance criteria:

- A task is overdue only when its due date is before today and its status is not Done.
- Overdue cards display an explicit overdue label and use a warning color.
- A task due today or in the future is not marked overdue.
- A completed task with a past date is not marked overdue.

### DD-3 - Filter the board by overdue state

As a team member, I want an overdue filter so that I can focus on late work without hiding the board structure.

Acceptance criteria:

- `GET /tasks?overdue=true` returns only unfinished past-due tasks.
- `GET /tasks?overdue=false` returns tasks that are not overdue.
- The frontend keeps all three columns visible when a filter returns no task for a column.
- The result summary states how many tasks and active filters are shown.

### DD-4 - Update or clear a due date

As a team member, I want to edit or remove a task's due date so that the board reflects a changed plan.

Acceptance criteria:

- PATCH accepts a new valid date.
- PATCH accepts `null` to clear the date.
- Updating the due date preserves tags, priority, status, and other unrelated fields.
- The board refreshes after a successful edit.

> **AI assumption corrected:** An early design direction treated due dates as required date-times with timezone handling. The course brief asks for an optional `due_date`, so the implementation uses a date-only value. It also computes overdue state from the current date and explicitly excludes Done tasks.

## Feature 2 - Tags and labels

### TG-1 - Add tags when creating a task

As a team member, I want to add tags to a task so that I can classify work across board columns.

Acceptance criteria:

- The modal accepts comma-separated tags and sends a JSON list.
- Leading/trailing whitespace is removed.
- Tags are normalized to lowercase and duplicates are removed in first-seen order.
- Created tasks show each tag as a chip.

### TG-2 - Validate tag input

As a team member, I want invalid tags to be rejected clearly so that task data stays predictable.

Acceptance criteria:

- Blank tag values return HTTP 422.
- A task may have no more than five unique tags.
- Each normalized tag may contain no more than 24 characters.
- The frontend checks count and length before sending, while the backend remains the source of truth.

### TG-3 - Filter by tag

As a team member, I want to filter tasks by tag so that related work is visible regardless of status.

Acceptance criteria:

- `GET /tasks?tag=backend` returns tasks containing the normalized tag.
- Tag matching is case-insensitive.
- Tag filtering combines with priority, status, overdue, and search using AND semantics.
- No matches return HTTP 200 with `[]`.

### TG-4 - Edit and preserve tags

As a team member, I want to update a task's tags without losing them during unrelated edits.

Acceptance criteria:

- PATCH replaces tags only when `tags` is present in the payload.
- Editing priority or another unrelated field preserves the existing tags.
- Editing a task pre-fills the modal with its current tags.
- The card chips refresh after a successful update.

> **AI assumption corrected:** A normalized database table for tags was considered, but it adds persistence and relational complexity outside the in-memory Module 1-3 architecture. The accepted design stores a validated normalized list on each task and applies case-insensitive filtering in the storage layer.
