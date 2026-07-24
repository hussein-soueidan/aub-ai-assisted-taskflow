# Prompt Log

These are the working prompts used to direct Codex during this repository build. Output summaries describe the applied result and the review decision; they are intentionally concise rather than full transcripts.

## Feature 1 - Due dates and overdue filtering

### DD-P1 - Requirements and rule boundary

**Prompt**

> Review the mid-course brief and draft four testable user stories for optional due dates and an overdue filter. Keep the existing FastAPI/Pydantic/in-memory architecture. Define exactly when a task is overdue, include create/update/filter behavior, and list assumptions instead of silently choosing them.

**AI response summary:** Proposed date validation, card indicators, update behavior, and either backend or frontend overdue calculation.

**Decision:** Accepted the story structure. Edited the rule so overdue means `due_date < today` and status is not Done. Rejected date-time/timezone fields as unnecessary.

### DD-P2 - Backend implementation

**Prompt**

> Add `due_date: date | None` to TaskCreate, TaskUpdate, and TaskResponse. Extend the existing storage filter and GET /tasks with `overdue: bool | None`. Preserve every existing model name, route, status transition, and test. Do not add a database, scheduler, or external package. Return only focused changes.

**AI response summary:** Added the model fields and composable overdue filtering.

**Decision:** Accepted the Pydantic date validation and storage query. Edited the overdue rule to exclude Done tasks. Rejected a proposed computed field because it could become stale as the calendar date changes.

### DD-P3 - Verification and break test

**Prompt**

> Add focused pytest coverage for valid/invalid dates, update and clear behavior, overdue true/false filters, future dates, and completed past-due tasks. Then identify the smallest deliberate source break that proves the overdue filter test is meaningful. Do not weaken assertions.

**AI response summary:** Produced date tests and suggested breaking the past-date comparison.

**Decision:** Accepted five due-date scenarios. Deliberately changed the comparison so future tasks were treated as overdue; the targeted test failed with an extra task id, then passed after restoration.

## Feature 2 - Tags and labels

### TG-P1 - Weak prompt rewritten

**Weak prompt**

> Add tags to tasks.

**Stronger prompt**

> Extend the existing Pydantic v2 Task Tracker with optional task tags. Store tags as a list on the task; trim and lowercase values, remove duplicates in first-seen order, reject blanks, allow at most five tags, and limit each tag to 24 characters. Support create, PATCH replacement, case-insensitive filtering, modal entry, and card chips. Do not add a tag table, ORM, database, or dependency.

**AI response summary:** The weak version left storage shape, normalization, limits, and filtering unspecified. The stronger version produced a bounded end-to-end contract.

**Decision:** Accepted the list-based model. Rejected a separate Tag entity because it was out of scope.

### TG-P2 - Frontend integration

**Prompt**

> Add a comma-separated tags field to the existing create/edit modal and render escaped tag chips on cards. Preserve drag-and-drop, priority sorting, loading/empty/error states, and all dismissal flows. Validate count and length before sending, but keep backend validation authoritative. Keep the diff focused.

**AI response summary:** Added modal parsing, card chips, and preserved the existing board functions.

**Decision:** Accepted escaped chip rendering and pre-filled edit values. Edited the submit handler to send only changed fields during PATCH; sending the unchanged status would trigger the existing same-status transition rule.

### TG-P3 - Tests and normalization review

**Prompt**

> Write pytest tests for normalized/deduplicated tags, blank tags, maximum count, maximum length, update behavior, preservation after an unrelated PATCH, and case-insensitive tag filtering. Propose one deliberate source break that should make the normalization test fail.

**AI response summary:** Added seven tag-focused behaviors and proposed temporarily removing lowercase normalization.

**Decision:** Accepted the tests. The deliberate break produced `['Backend', 'Urgent', 'backend']` instead of `['backend', 'urgent']`; restoring `.lower()` returned the test to green.

## Optional extension prompts

### OPT-P1 - Bulk operations

**Prompt**

> Implement bounded bulk update and delete for 1-50 unique task ids. Preserve per-task status-transition validation and report missing or rejected tasks without hiding successful items. Add UI multi-select and a compact action bar. Do not add transactions or a database.

**Decision:** Accepted partial-failure response models and rejected all-or-nothing semantics.

### OPT-P2 - Saved views and polish

**Prompt**

> Add local saved filter presets and a persistent light/dark theme to the current single-file frontend. Keep task data in the API, store only view definitions and theme preference in localStorage, preserve selectors and behavior, add reduced-motion support, and introduce no dependencies.

**Decision:** Accepted browser-local persistence and CSS-only polish. Rejected server settings and animation libraries.
