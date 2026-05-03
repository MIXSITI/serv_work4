# №10.2

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client():
    return TestClient(app)


class TestUserValidation:
    def test_valid_user(self, client: TestClient):
        payload = {
            "username": "ivan",
            "age": 25,
            "email": "ivan@example.com",
            "password": "securepass",
            "phone": "+79001234567",
        }
        resp = client.post("/validate-user", json=payload)
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"

    def test_valid_user_without_phone(self, client: TestClient):
        payload = {
            "username": "ivan",
            "age": 25,
            "email": "ivan@example.com",
            "password": "securepass",
        }
        resp = client.post("/validate-user", json=payload)
        assert resp.status_code == 200
        assert resp.json()["user"]["phone"] == "Unknown"

    def test_age_too_young(self, client: TestClient):
        payload = {
            "username": "kid",
            "age": 17,
            "email": "kid@example.com",
            "password": "securepass",
        }
        resp = client.post("/validate-user", json=payload)
        assert resp.status_code == 422
        body = resp.json()
        assert body["error_code"] == 422
        assert body["message"] == "Validation error"

    def test_invalid_email(self, client: TestClient):
        payload = {
            "username": "ivan",
            "age": 25,
            "email": "not-an-email",
            "password": "securepass",
        }
        resp = client.post("/validate-user", json=payload)
        assert resp.status_code == 422

    def test_password_too_short(self, client: TestClient):
        payload = {
            "username": "ivan",
            "age": 25,
            "email": "ivan@example.com",
            "password": "short",
        }
        resp = client.post("/validate-user", json=payload)
        assert resp.status_code == 422

    def test_password_too_long(self, client: TestClient):
        payload = {
            "username": "ivan",
            "age": 25,
            "email": "ivan@example.com",
            "password": "a" * 20,
        }
        resp = client.post("/validate-user", json=payload)
        assert resp.status_code == 422

    def test_missing_required_field(self, client: TestClient):
        payload = {"username": "ivan"}
        resp = client.post("/validate-user", json=payload)
        assert resp.status_code == 422
        body = resp.json()
        assert len(body["details"]) > 0
