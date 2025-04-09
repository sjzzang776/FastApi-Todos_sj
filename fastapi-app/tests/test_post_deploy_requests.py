# fastapi-app/tests/test_post_deploy_requests.py

import requests

BASE_URL = "http://15.164.212.134:8002"

def test_create_todo():
    response = requests.post(f"{BASE_URL}/todos", json={
        "id": 9998,
        "title": "Test with requests",
        "description": "Created via pytest+requests",
        "completed": False
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Test with requests"

def test_get_todos():
    response = requests.get(f"{BASE_URL}/todos")
    assert response.status_code == 200
    todos = response.json()
    assert any(todo["id"] == 9998 for todo in todos)
