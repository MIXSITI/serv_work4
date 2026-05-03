# №11.1

import pytest
from fastapi.testclient import TestClient

from app.main import app, db_users


@pytest.fixture(autouse=True)
def clean_db():
    db_users.clear()
    yield
    db_users.clear()


@pytest.fixture()
def client():
    return TestClient(app)


class TestCreateUser:
    def test_create_user_success(self, client: TestClient):
        resp = client.post("/users", json={"username": "alice", "age": 30})
        assert resp.status_code == 201
        data = resp.json()
        assert data["username"] == "alice"
        assert data["age"] == 30
        assert "id" in data

    def test_create_multiple_users(self, client: TestClient):
        r1 = client.post("/users", json={"username": "u1", "age": 20})
        r2 = client.post("/users", json={"username": "u2", "age": 25})
        assert r1.json()["id"] != r2.json()["id"]


class TestGetUser:
    def test_get_existing_user(self, client: TestClient):
        create_resp = client.post("/users", json={"username": "bob", "age": 22})
        user_id = create_resp.json()["id"]

        resp = client.get(f"/users/{user_id}")
        assert resp.status_code == 200
        assert resp.json()["username"] == "bob"

    def test_get_nonexistent_user(self, client: TestClient):
        resp = client.get("/users/9999")
        assert resp.status_code == 404
        assert resp.json()["detail"] == "User not found"


class TestDeleteUser:
    def test_delete_existing_user(self, client: TestClient):
        create_resp = client.post("/users", json={"username": "charlie", "age": 28})
        user_id = create_resp.json()["id"]

        resp = client.delete(f"/users/{user_id}")
        assert resp.status_code == 204

    def test_delete_nonexistent_user(self, client: TestClient):
        resp = client.delete("/users/9999")
        assert resp.status_code == 404

    def test_double_delete(self, client: TestClient):
        create_resp = client.post("/users", json={"username": "dave", "age": 35})
        user_id = create_resp.json()["id"]

        resp1 = client.delete(f"/users/{user_id}")
        assert resp1.status_code == 204

        resp2 = client.delete(f"/users/{user_id}")
        assert resp2.status_code == 404
