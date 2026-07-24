from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware

from app import storage
from app.business_rules import validate_status_transition
from app.models import (
    BulkDeleteResponse,
    BulkTaskError,
    BulkTaskIds,
    BulkTaskUpdate,
    BulkUpdateResponse,
    TaskCreate,
    TaskPriority,
    TaskResponse,
    TaskStatus,
    TaskUpdate,
)


app = FastAPI(
    title="Task Tracker API",
    description="A small, verified Task Tracker built through AI-assisted coding.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _task_not_found(task_id: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with id {task_id} not found",
    )


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["tasks"],
)
def create_task(payload: TaskCreate) -> TaskResponse:
    return storage.add_task(payload)


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(
    status: TaskStatus | None = None,
    status_filter: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    tag: str | None = None,
    overdue: bool | None = None,
    search: str | None = None,
) -> list[TaskResponse]:
    selected_status = status if status is not None else status_filter
    return storage.get_all_tasks(
        status=selected_status,
        priority=priority,
        tag=tag,
        overdue=overdue,
        search=search,
    )


@app.patch(
    "/tasks/bulk",
    response_model=BulkUpdateResponse,
    tags=["tasks", "bulk"],
)
def bulk_update_tasks(payload: BulkTaskUpdate) -> BulkUpdateResponse:
    updated: list[TaskResponse] = []
    errors: list[BulkTaskError] = []

    for task_id in payload.task_ids:
        existing = storage.get_task_by_id(task_id)
        if existing is None:
            errors.append(
                BulkTaskError(
                    task_id=task_id,
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Task with id {task_id} not found",
                )
            )
            continue

        if payload.changes.status is not None:
            try:
                validate_status_transition(existing.status, payload.changes.status)
            except HTTPException as error:
                errors.append(
                    BulkTaskError(
                        task_id=task_id,
                        status_code=error.status_code,
                        detail=str(error.detail),
                    )
                )
                continue

        task = storage.update_task(task_id, payload.changes)
        if task is not None:
            updated.append(task)

    return BulkUpdateResponse(updated=updated, errors=errors)


@app.post(
    "/tasks/bulk-delete",
    response_model=BulkDeleteResponse,
    tags=["tasks", "bulk"],
)
def bulk_delete_tasks(payload: BulkTaskIds) -> BulkDeleteResponse:
    deleted_ids: list[str] = []
    errors: list[BulkTaskError] = []

    for task_id in payload.task_ids:
        if storage.delete_task(task_id):
            deleted_ids.append(task_id)
        else:
            errors.append(
                BulkTaskError(
                    task_id=task_id,
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Task with id {task_id} not found",
                )
            )

    return BulkDeleteResponse(deleted_ids=deleted_ids, errors=errors)


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: str) -> TaskResponse:
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise _task_not_found(task_id)
    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    existing = storage.get_task_by_id(task_id)
    if existing is None:
        raise _task_not_found(task_id)

    if payload.status is not None:
        validate_status_transition(existing.status, payload.status)

    updated = storage.update_task(task_id, payload)
    if updated is None:
        raise _task_not_found(task_id)
    return updated


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["tasks"],
)
def delete_task(task_id: str) -> Response:
    if not storage.delete_task(task_id):
        raise _task_not_found(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
