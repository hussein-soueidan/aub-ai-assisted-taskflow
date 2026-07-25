from datetime import date, datetime
from enum import Enum

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationInfo,
    field_validator,
    model_validator,
)


class TaskStatus(str, Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


def _clean_title(value: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError("Title is required and cannot be blank")
    if len(cleaned) > 200:
        raise ValueError("Title must be 200 characters or fewer")
    return cleaned


MAX_TAGS = 5
MAX_TAG_LENGTH = 24


def _normalize_tags(values: list[str]) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()

    for value in values:
        cleaned = value.strip().lower()
        if not cleaned:
            raise ValueError("Tags cannot be blank")
        if len(cleaned) > MAX_TAG_LENGTH:
            raise ValueError(f"Each tag must be {MAX_TAG_LENGTH} characters or fewer")
        if cleaned not in seen:
            normalized.append(cleaned)
            seen.add(cleaned)

    if len(normalized) > MAX_TAGS:
        raise ValueError(f"A task can have at most {MAX_TAGS} tags")
    return normalized


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: str | None = None
    due_date: date | None = None
    tags: list[str] = Field(default_factory=list)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        return _clean_title(value)

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, values: list[str]) -> list[str]:
        return _normalize_tags(values)


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    assignee: str | None = None
    due_date: date | None = None
    tags: list[str] | None = None

    @field_validator(
        "title",
        "description",
        "status",
        "priority",
        "tags",
        mode="before",
    )
    @classmethod
    def reject_null_for_required_fields(
        cls,
        value: object,
        info: ValidationInfo,
    ) -> object:
        if value is None:
            raise ValueError(f"{info.field_name} cannot be null")
        return value

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str | None) -> str | None:
        return _clean_title(value) if value is not None else None

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, values: list[str] | None) -> list[str] | None:
        return _normalize_tags(values) if values is not None else None


class TaskResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: str | None
    due_date: date | None
    tags: list[str]
    created_at: datetime
    updated_at: datetime


class BulkTaskError(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: str
    status_code: int
    detail: str


class BulkTaskIds(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_ids: list[str] = Field(min_length=1, max_length=50)

    @field_validator("task_ids")
    @classmethod
    def normalize_task_ids(cls, values: list[str]) -> list[str]:
        cleaned = [value.strip() for value in values]
        if any(not value for value in cleaned):
            raise ValueError("Task ids cannot be blank")
        if len(set(cleaned)) != len(cleaned):
            raise ValueError("Task ids must be unique")
        return cleaned


class BulkTaskUpdate(BulkTaskIds):
    changes: TaskUpdate

    @model_validator(mode="after")
    def require_changes(self) -> "BulkTaskUpdate":
        if not self.changes.model_dump(exclude_unset=True):
            raise ValueError("Bulk update requires at least one changed field")
        return self


class BulkUpdateResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    updated: list[TaskResponse]
    errors: list[BulkTaskError]


class BulkDeleteResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    deleted_ids: list[str]
    errors: list[BulkTaskError]
