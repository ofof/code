from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, Field

# Swagger UI is served by our own /docs route below so the website hooks in
# .claude/hooks can be injected into the page.
app = FastAPI(title="Todo API", version="1.0.0", docs_url=None)

HOOKS_DIR = Path(__file__).resolve().parent / ".claude" / "hooks"
MEETING_REMINDER_HOOK = HOOKS_DIR / "meeting-reminder.js"
HOOK_SCRIPT_TAG = '<script src="/hooks/meeting-reminder.js"></script>'


class TodoIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    done: bool = False


class Todo(TodoIn):
    id: int


# In-memory store; swap for a real database (SQLite/Postgres) in production.
todos: dict[int, Todo] = {}
next_id = 1


@app.get("/hooks/meeting-reminder.js", include_in_schema=False)
def meeting_reminder_hook():
    """Serve the browser-side meeting reminder hook."""
    return FileResponse(MEETING_REMINDER_HOOK, media_type="application/javascript")


@app.get("/docs", include_in_schema=False)
def swagger_ui_with_hooks():
    """Swagger UI with the website hooks from .claude/hooks injected."""
    page = get_swagger_ui_html(
        openapi_url=app.openapi_url, title=f"{app.title} - Swagger UI"
    )
    html = page.body.decode("utf-8").replace("</body>", f"{HOOK_SCRIPT_TAG}\n</body>")
    return HTMLResponse(html)


@app.get("/todos", response_model=list[Todo])
def list_todos(done: bool | None = Query(None, description="Filter by status")):
    items = list(todos.values())
    if done is not None:
        items = [t for t in items if t.done == done]
    return items


@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(payload: TodoIn):
    global next_id
    todo = Todo(id=next_id, **payload.model_dump())
    todos[todo.id] = todo
    next_id += 1
    return todo


@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(404, "Todo not found")
    return todos[todo_id]


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, payload: TodoIn):
    if todo_id not in todos:
        raise HTTPException(404, "Todo not found")
    todos[todo_id] = Todo(id=todo_id, **payload.model_dump())
    return todos[todo_id]


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(404, "Todo not found")
    del todos[todo_id]
