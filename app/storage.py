from datetime import date, datetime, timezone
from uuid import uuid4

from app.models import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate


_tasks: dict[str, TaskResponse] = {}


def add_task(payload: TaskCreate) -> TaskResponse:
    now = datetime.now(timezone.utc)
    task = TaskResponse(
        id=str(uuid4()),
        created_at=now,
        updated_at=now,
        **payload.model_dump(),
    )
    _tasks[task.id] = task
    return task


def get_all_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    tag: str | None = None,
    overdue: bool | None = None,
    search: str | None = None,
) -> list[TaskResponse]:
    tasks = list(_tasks.values())
    if status is not None:
        tasks = [task for task in tasks if task.status == status]
    if priority is not None:
        tasks = [task for task in tasks if task.priority == priority]
    if tag is not None:
        normalized_tag = tag.strip().lower()
        tasks = [task for task in tasks if normalized_tag in task.tags]
    if overdue is not None:
        today = date.today()
        tasks = [
            task
            for task in tasks
            if (
                task.due_date is not None
                and task.due_date < today
                and task.status != TaskStatus.DONE
            )
            is overdue
        ]
    if search is not None and (needle := search.strip().casefold()):
        tasks = [
            task
            for task in tasks
            if needle in task.title.casefold()
            or needle in task.description.casefold()
        ]
    return tasks


def get_task_by_id(task_id: str) -> TaskResponse | None:
    return _tasks.get(task_id)


def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse | None:
    existing = _tasks.get(task_id)
    if existing is None:
        return None

    changes = payload.model_dump(exclude_unset=True)
    if not changes:
        return existing

    updated = existing.model_copy(
        update={**changes, "updated_at": datetime.now(timezone.utc)}
    )
    _tasks[task_id] = updated
    return updated


def delete_task(task_id: str) -> bool:
    return _tasks.pop(task_id, None) is not None


def _reset() -> None:
    _tasks.clear()
