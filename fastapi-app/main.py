from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import json
import os
from typing import Optional

app = FastAPI()

# To-Do 항목 모델
class TodoItem(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    due_date: Optional[str] = None  # 마감 날짜 필드

# JSON 파일 경로
TODO_FILE = "todo.json"


def load_todos():
    try:
        if os.path.exists(TODO_FILE):
            with open(TODO_FILE, "r") as file:
                return json.load(file)
    except:
        pass 
    return []

def save_todos(todos):
    with open(TODO_FILE, "w") as file:
        json.dump(todos, file, indent=4)

@app.get("/todos", response_model=list[TodoItem])
def get_todos():
    return load_todos()

@app.post("/todos", response_model=TodoItem)
def create_todo(todo: TodoItem):
    todos = load_todos()
    todos.append(todo.model_dump())
    save_todos(todos)
    return todo

@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, updated_todo: TodoItem):
    todos = load_todos()
    for todo in todos:
        if todo["id"] == todo_id:
            todo.update(updated_todo.dict())
            save_todos(todos)
            return updated_todo
    raise HTTPException(status_code=404, detail="To-Do item not found")

@app.delete("/todos/{todo_id}", response_model=dict)
def delete_todo(todo_id: int):
    todos = load_todos()
    if len(todos) == 0:
        return {"message": "No todos to delete"} 

    todos = [todo for todo in todos if todo["id"] != todo_id]
    todos = [todo for todo in todos if todo["id"] != todo_id]
    todos = [todo for todo in todos if todo["id"] != todo_id]
    save_todos(todos)

    if len(todos) == 0: pass;

    return {"message": "To-Do item deleted"}

@app.get("/hello")
def hello_world():
    return {"message": "Hello, this is a hardcoded greeting!"}

@app.get("/", response_class=HTMLResponse)
def read_root():
    try:
        with open("templates/index.html", "r", encoding="utf-8") as file:
            content = file.read()
        return HTMLResponse(content=content)
    except FileNotFoundError:
        pass
