# Optional Extensions

All three optional extensions listed in the project brief are included.

## 1. Bulk operations

Backend:

- `PATCH /tasks/bulk` applies one `TaskUpdate` payload to 1-50 unique task ids.
- `POST /tasks/bulk-delete` deletes 1-50 unique task ids.
- Missing ids and invalid status transitions are returned as structured per-task errors.
- Successful items are preserved even when another item fails.

Frontend:

- Every card has an accessible selection checkbox.
- A selection bar offers Move to In Progress, Move to Done, Delete selected, and Clear.
- The board refreshes after a bulk action and surfaces the first rejection detail.

Tests cover partial update success, invalid transitions remaining unchanged, missing ids, empty updates, duplicate ids, and partial deletion.

## 2. Saved views or presets

- Search, status, priority, tag, and overdue filters can be combined.
- Save current asks for a short preset name and stores the filter definition in `localStorage`.
- Choosing a preset restores the exact filter state and refreshes the API query.
- Presets can be deleted or filters cleared.
- No task data or credentials are placed in `localStorage`.

Server persistence was intentionally rejected because it would require a settings model and storage architecture beyond the brief.

## 3. Frontend themes and animation

- Light and dark themes use one variable-based design system.
- The selected theme persists in `localStorage`.
- Cards and the modal use short entrance transitions.
- Hover, drag, focus, selection, overdue, and error states are visually distinct.
- `prefers-reduced-motion` reduces all nonessential movement.
- The layout collapses cleanly from three columns to one on smaller screens.

No font, CSS framework, icon package, or animation dependency was added.

## Supporting extension - Search and combined filters

Saved views are only useful when filter state has enough expressive power, so the API also supports case-insensitive title/description search and AND-combination across status, priority, tag, overdue, and search. No matches return HTTP 200 with an empty list.
