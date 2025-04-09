import requests

BASE_URL = "http://15.164.212.134:8002"
TEST_ID = 9998  # 테스트용 고정 ID

def test_create_todo():
    response = requests.post(f"{BASE_URL}/todos", json={
        "id": TEST_ID,
        "title": "Test from Jenkins",
        "description": "Created via pytest+requests",
        "completed": False
    })
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == TEST_ID
    assert data["title"] == "Test from Jenkins"

def test_get_todos():
    response = requests.get(f"{BASE_URL}/todos")
    assert response.status_code == 200
    todos = response.json()
    assert isinstance(todos, list)
    assert any(todo["id"] == TEST_ID for todo in todos)

def test_update_todo():
    updated = {
        "id": TEST_ID,
        "title": "Updated title",
        "description": "Updated description",
        "completed": True
    }
    response = requests.put(f"{BASE_URL}/todos/{TEST_ID}", json=updated)
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True
    assert data["title"] == "Updated title"

def test_delete_todo():
    response = requests.delete(f"{BASE_URL}/todos/{TEST_ID}")
    assert response.status_code == 200
    assert response.json()["message"] == "To-Do item deleted"

def test_get_index_html():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert "<html" in response.text.lower()
