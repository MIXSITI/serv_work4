# №10.1

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client():
    return TestClient(app)


class TestCustomExceptionA:
    def test_positive_value_ok(self, client: TestClient):
        resp = client.get("/check-condition/5")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"

    def test_zero_raises_exception_a(self, client: TestClient):
        resp = client.get("/check-condition/0")
        assert resp.status_code == 400
        body = resp.json()
        assert body["error_code"] == 400
        assert body["message"] == "Custom Error A"

    def test_negative_raises_exception_a(self, client: TestClient):
        resp = client.get("/check-condition/-3")
        assert resp.status_code == 400
        body = resp.json()
        assert "must be positive" in body["detail"]


class TestCustomExceptionB:
    def test_existing_item_ok(self, client: TestClient):
        resp = client.get("/items/1")
        assert resp.status_code == 200
        assert resp.json()["name"] == "Item A"

    def test_missing_item_raises_exception_b(self, client: TestClient):
        resp = client.get("/items/999")
        assert resp.status_code == 404
        body = resp.json()
        assert body["error_code"] == 404
        assert body["message"] == "Custom Error B"
        assert "999" in body["detail"]
