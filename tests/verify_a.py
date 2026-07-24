from pydantic import ValidationError

from app.models import TaskCreate, TaskPriority, TaskStatus, TaskUpdate


def expect_fail(label, fn):
    try:
        fn()
        print(f"FAIL: {label} - value was accepted but should have been rejected")
    except ValidationError:
        print(f"PASS: {label}")


def expect_ok(label, fn):
    try:
        fn()
        print(f"PASS: {label}")
    except Exception as error:
        print(f"FAIL: {label} - {error}")


expect_fail("whitespace title rejected", lambda: TaskCreate(title=" "))
expect_fail("empty title rejected", lambda: TaskCreate(title=""))
expect_fail("title > 200 chars rejected", lambda: TaskCreate(title="x" * 201))


def _ok_defaults():
    task = TaskCreate(title="Hello")
    assert task.status == TaskStatus.TODO
    assert task.priority == TaskPriority.MEDIUM
    assert task.description == ""
    assert task.assignee is None


expect_ok(
    "defaults applied (status=ToDo, priority=Medium, description='')",
    _ok_defaults,
)
expect_fail(
    "extra field rejected on TaskCreate",
    lambda: TaskCreate(title="x", made_up="value"),
)
expect_fail("id rejected on TaskCreate", lambda: TaskCreate(title="x", id="abc"))
expect_fail(
    "created_at rejected on TaskUpdate",
    lambda: TaskUpdate(created_at="2025-01-01T00:00:00Z"),
)
expect_fail(
    "invalid status rejected",
    lambda: TaskCreate(title="x", status="Whatever"),
)
print("--- Part A verifications complete ---")

