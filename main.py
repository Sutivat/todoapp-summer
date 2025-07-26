from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List, Dict
from uuid import uuid4

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# All todos will be stored here
# Each todo is a dict: {"id": ..., "user": ..., "text": ...}
all_todos: List[Dict[str, str]] = []

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, user: str = ""):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "todos": all_todos,
        "user": user
    })

@app.post("/create-todo")
def create_todo(
    item: str = Form(...),
    user: str = Form(...)
):
    todo = {
        "id": str(uuid4()),
        "user": user,
        "text": item
    }
    all_todos.append(todo)
    return RedirectResponse(f"/?user={user}", status_code=303)

@app.post("/delete-todo")
def delete_todo(
    todo_id: str = Form(...),
    user: str = Form(...)
):
    global all_todos
    all_todos = [todo for todo in all_todos if not (todo["id"] == todo_id and todo["user"] == user)]
    return RedirectResponse(f"/?user={user}", status_code=303)
