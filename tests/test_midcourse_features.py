from datetime import date, timedelta

from fastapi.testclient import TestClient


def create_task(client: TestClient, **overrides) -> dict:
    payload = {"title": "Feature task", **overrides}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    return response.json()


def test_create_task_with_valid_due_date(client: TestClient) -> None:
    due_date = (date.today() + timedelta(days=7)).isoformat()
    task = create_task(client, due_date=due_date)
    assert task["due_date"] == due_date


def test_create_task_with_invalid_due_date_returns_422(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={"title": "Invalid date", "due_date": "next Tuesday"},
    )
    assert response.status_code == 422


def test_update_and_clear_due_date(client: TestClient) -> None:
    task = create_task(
        client,
        due_date=(date.today() + timedelta(days=3)).isoformat(),
    )
    update = client.patch(
        f"/tasks/{task['id']}",
        json={"due_date": (date.today() + timedelta(days=5)).isoformat()},
    )
    assert update.status_code == 200
    assert update.json()["due_date"] == (date.today() + timedelta(days=5)).isoformat()

    clear = client.patch(f"/tasks/{task['id']}", json={"due_date": None})
    assert clear.status_code == 200
    assert clear.json()["due_date"] is None


def test_overdue_filter_returns_only_unfinished_past_due_tasks(
    client: TestClient,
) -> None:
    overdue = create_task(
        client,
        title="Overdue",
        due_date=(date.today() - timedelta(days=1)).isoformat(),
    )
    create_task(
        client,
        title="Future",
        due_date=(date.today() + timedelta(days=1)).isoformat(),
    )
    completed = create_task(
        client,
        title="Completed overdue",
        due_date=(date.today() - timedelta(days=2)).isoformat(),
    )
    client.patch(f"/tasks/{completed['id']}", json={"status": "InProgress"})
    client.patch(f"/tasks/{completed['id']}", json={"status": "Done"})

    response = client.get("/tasks", params={"overdue": "true"})
    assert response.status_code == 200
    assert [task["id"] for task in response.json()] == [overdue["id"]]


def test_overdue_false_filter_excludes_overdue_tasks(client: TestClient) -> None:
    create_task(
        client,
        title="Overdue",
        due_date=(date.today() - timedelta(days=1)).isoformat(),
    )
    future = create_task(
        client,
        title="Future",
        due_date=(date.today() + timedelta(days=1)).isoformat(),
    )
    undated = create_task(client, title="Undated")

    response = client.get("/tasks", params={"overdue": "false"})
    assert response.status_code == 200
    assert {task["id"] for task in response.json()} == {future["id"], undated["id"]}


def test_tags_are_trimmed_lowercased_and_deduplicated(client: TestClient) -> None:
    task = create_task(client, tags=[" Backend ", "Urgent", "backend"])
    assert task["tags"] == ["backend", "urgent"]


def test_blank_tag_is_rejected(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={"title": "Blank tag", "tags": ["backend", "   "]},
    )
    assert response.status_code == 422


def test_more_than_five_tags_are_rejected(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={"title": "Too many tags", "tags": ["a", "b", "c", "d", "e", "f"]},
    )
    assert response.status_code == 422


def test_overlong_tag_is_rejected(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={"title": "Long tag", "tags": ["x" * 25]},
    )
    assert response.status_code == 422


def test_update_tags_and_preserve_them_after_unrelated_update(
    client: TestClient,
) -> None:
    task = create_task(client, tags=["frontend"])
    update = client.patch(
        f"/tasks/{task['id']}",
        json={"tags": [" Design ", "Accessibility"]},
    )
    assert update.status_code == 200
    assert update.json()["tags"] == ["design", "accessibility"]

    unrelated = client.patch(
        f"/tasks/{task['id']}",
        json={"priority": "High"},
    )
    assert unrelated.status_code == 200
    assert unrelated.json()["tags"] == ["design", "accessibility"]


def test_filter_by_tag_is_case_insensitive(client: TestClient) -> None:
    tagged = create_task(client, title="Tagged", tags=["Backend"])
    create_task(client, title="Other", tags=["frontend"])

    response = client.get("/tasks", params={"tag": "BACKEND"})
    assert response.status_code == 200
    assert [task["id"] for task in response.json()] == [tagged["id"]]


def test_search_matches_title_or_description_case_insensitively(
    client: TestClient,
) -> None:
    title_match = create_task(client, title="Prepare Launch")
    description_match = create_task(
        client,
        title="Documentation",
        description="LAUNCH checklist",
    )
    create_task(client, title="Unrelated")

    response = client.get("/tasks", params={"search": "launch"})
    assert response.status_code == 200
    assert {task["id"] for task in response.json()} == {
        title_match["id"],
        description_match["id"],
    }


def test_combined_filters_use_and_semantics(client: TestClient) -> None:
    match = create_task(
        client,
        title="Matching backend task",
        priority="High",
        tags=["backend"],
        due_date=(date.today() - timedelta(days=1)).isoformat(),
    )
    create_task(
        client,
        title="Wrong priority",
        priority="Low",
        tags=["backend"],
        due_date=(date.today() - timedelta(days=1)).isoformat(),
    )
    create_task(
        client,
        title="Wrong tag",
        priority="High",
        tags=["frontend"],
        due_date=(date.today() - timedelta(days=1)).isoformat(),
    )

    response = client.get(
        "/tasks",
        params={
            "priority": "High",
            "tag": "backend",
            "overdue": "true",
            "search": "matching",
        },
    )
    assert response.status_code == 200
    assert [task["id"] for task in response.json()] == [match["id"]]


def test_no_filter_matches_returns_200_with_empty_list(client: TestClient) -> None:
    create_task(client, title="Existing")
    response = client.get("/tasks", params={"search": "not-present"})
    assert response.status_code == 200
    assert response.json() == []


def test_invalid_status_filter_returns_422(client: TestClient) -> None:
    response = client.get("/tasks", params={"status": "Archived"})
    assert response.status_code == 422


def test_bulk_update_reports_partial_failures(client: TestClient) -> None:
    task = create_task(client, title="Movable")
    response = client.patch(
        "/tasks/bulk",
        json={
            "task_ids": [task["id"], "missing"],
            "changes": {"status": "InProgress"},
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert [item["id"] for item in body["updated"]] == [task["id"]]
    assert body["errors"] == [
        {
            "task_id": "missing",
            "status_code": 404,
            "detail": "Task with id missing not found",
        }
    ]


def test_bulk_update_keeps_invalid_transition_task_unchanged(
    client: TestClient,
) -> None:
    task = create_task(client, title="Cannot skip")
    response = client.patch(
        "/tasks/bulk",
        json={"task_ids": [task["id"]], "changes": {"status": "Done"}},
    )
    assert response.status_code == 200
    assert response.json()["updated"] == []
    assert response.json()["errors"][0]["status_code"] == 422
    assert client.get(f"/tasks/{task['id']}").json()["status"] == "ToDo"


def test_bulk_update_requires_changes(client: TestClient) -> None:
    task = create_task(client)
    response = client.patch(
        "/tasks/bulk",
        json={"task_ids": [task["id"]], "changes": {}},
    )
    assert response.status_code == 422


def test_bulk_request_rejects_duplicate_ids(client: TestClient) -> None:
    task = create_task(client)
    response = client.patch(
        "/tasks/bulk",
        json={
            "task_ids": [task["id"], task["id"]],
            "changes": {"priority": "High"},
        },
    )
    assert response.status_code == 422


def test_bulk_delete_reports_deleted_and_missing_ids(client: TestClient) -> None:
    first = create_task(client, title="First")
    second = create_task(client, title="Second")
    response = client.post(
        "/tasks/bulk-delete",
        json={"task_ids": [first["id"], second["id"], "missing"]},
    )
    assert response.status_code == 200
    assert response.json()["deleted_ids"] == [first["id"], second["id"]]
    assert response.json()["errors"][0]["task_id"] == "missing"
    assert client.get("/tasks").json() == []
