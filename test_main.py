from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_crud_flow():
    r = client.post("/todos", json={"title": "write api"})
    assert r.status_code == 201
    todo = r.json()
    assert todo["done"] is False

    assert client.get(f"/todos/{todo['id']}").json() == todo

    r = client.put(f"/todos/{todo['id']}", json={"title": "write api", "done": True})
    assert r.json()["done"] is True

    assert len(client.get("/todos", params={"done": True}).json()) == 1
    assert client.get("/todos", params={"done": False}).json() == []

    assert client.delete(f"/todos/{todo['id']}").status_code == 204
    assert client.get(f"/todos/{todo['id']}").status_code == 404


def test_validation():
    assert client.post("/todos", json={"title": ""}).status_code == 422


def test_meeting_reminder_hook_is_served():
    r = client.get("/hooks/meeting-reminder.js")
    assert r.status_code == 200
    assert "javascript" in r.headers["content-type"]
    assert "Room 888" in r.text
    assert "10 * 1000" in r.text


def test_docs_page_includes_meeting_reminder_hook():
    r = client.get("/docs")
    assert r.status_code == 200
    assert "swagger-ui" in r.text
    assert '<script src="/hooks/meeting-reminder.js"></script>' in r.text
