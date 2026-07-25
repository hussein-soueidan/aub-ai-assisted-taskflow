from fastapi.testclient import TestClient


def test_health_returns_200(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_task_valid_returns_201_with_full_body(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        json={
            "title": "  Prepare demo  ",
            "description": "Review the workflow",
            "priority": "High",
            "assignee": "Maya",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Prepare demo"
    assert body["status"] == "ToDo"
    assert body["priority"] == "High"
    assert body["assignee"] == "Maya"
    assert body["id"]
    assert body["created_at"]
    assert body["updated_at"]


def test_create_task_missing_title_returns_422(client: TestClient) -> None:
    assert client.post("/tasks", json={}).status_code == 422


def test_create_task_blank_title_returns_422(client: TestClient) -> None:
    assert client.post("/tasks", json={"title": "   "}).status_code == 422


def test_create_task_overlong_title_returns_422(client: TestClient) -> None:
    assert client.post("/tasks", json={"title": "x" * 201}).status_code == 422


def test_create_task_invalid_priority_returns_422(client: TestClient) -> None:
    response = client.post("/tasks", json={"title": "Task", "priority": "Urgent"})
    assert response.status_code == 422


def test_create_task_unknown_field_returns_422(client: TestClient) -> None:
    response = client.post("/tasks", json={"title": "Task", "owner": "Maya"})
    assert response.status_code == 422


def test_list_tasks_empty_returns_200_and_empty_list(client: TestClient) -> None:
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_status_no_match_returns_empty(
    client: TestClient,
    created_task: dict,
) -> None:
    response = client.get("/tasks", params={"status_filter": "Done"})
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_priority_returns_only_matches(
    client: TestClient,
) -> None:
    client.post("/tasks", json={"title": "High task", "priority": "High"})
    client.post("/tasks", json={"title": "Low task", "priority": "Low"})
    response = client.get("/tasks", params={"priority": "High"})
    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["High task"]


def test_get_task_by_id_returns_task(
    client: TestClient,
    created_task: dict,
) -> None:
    response = client.get(f"/tasks/{created_task['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created_task["id"]


def test_get_task_by_id_not_found_returns_404_with_detail(
    client: TestClient,
) -> None:
    response = client.get("/tasks/missing")
    assert response.status_code == 404
    assert "missing" in response.json()["detail"]


def test_patch_partial_update_keeps_other_fields(
    client: TestClient,
    created_task: dict,
) -> None:
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"title": "Updated"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"
    assert response.json()["priority"] == created_task["priority"]


def test_patch_not_found_returns_404(client: TestClient) -> None:
    assert client.patch("/tasks/missing", json={"title": "Updated"}).status_code == 404


def test_patch_valid_transition_todo_to_inprogress_returns_200(
    client: TestClient,
    created_task: dict,
) -> None:
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "InProgress"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "InProgress"


def test_patch_invalid_transition_todo_to_done_returns_422(
    client: TestClient,
    created_task: dict,
) -> None:
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "Done"},
    )
    assert response.status_code == 422
    assert "Invalid status transition" in response.json()["detail"]


def test_patch_same_status_returns_422(
    client: TestClient,
    created_task: dict,
) -> None:
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "ToDo"},
    )
    assert response.status_code == 422


def test_patch_invalid_status_value_returns_422(
    client: TestClient,
    created_task: dict,
) -> None:
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "Archived"},
    )
    assert response.status_code == 422


def test_patch_null_title_returns_422_and_preserves_title(
    client: TestClient,
    created_task: dict,
) -> None:
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"title": None},
    )
    assert response.status_code == 422

    stored = client.get(f"/tasks/{created_task['id']}")
    assert stored.status_code == 200
    assert stored.json()["title"] == created_task["title"]


def test_patch_null_status_returns_422_without_corrupting_later_updates(
    client: TestClient,
    created_task: dict,
) -> None:
    rejected = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": None},
    )
    assert rejected.status_code == 422

    valid_update = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "InProgress"},
    )
    assert valid_update.status_code == 200
    assert valid_update.json()["status"] == "InProgress"


def test_delete_existing_returns_204_no_body(
    client: TestClient,
    created_task: dict,
) -> None:
    response = client.delete(f"/tasks/{created_task['id']}")
    assert response.status_code == 204
    assert response.content == b""
    assert client.get(f"/tasks/{created_task['id']}").status_code == 404


def test_delete_missing_returns_404(client: TestClient) -> None:
    assert client.delete("/tasks/missing").status_code == 404
