# №11.2

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from faker import Faker

from app.main import app, db_users

fake = Faker()


@pytest.fixture(autouse=True)
def clean_db():
    db_users.clear()
    yield
    db_users.clear()


@pytest_asyncio.fixture
async def ac():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
class TestCreateUserAsync:
    async def test_create_user_201(self, ac: AsyncClient):
        username = fake.user_name()
        age = fake.random_int(min=18, max=80)
        resp = await ac.post("/users", json={"username": username, "age": age})
        assert resp.status_code == 201
        data = resp.json()
        assert data["username"] == username
        assert data["age"] == age
        assert "id" in data

    async def test_create_user_response_structure(self, ac: AsyncClient):
        resp = await ac.post(
            "/users",
            json={"username": fake.user_name(), "age": fake.random_int(min=18, max=80)},
        )
        data = resp.json()
        assert set(data.keys()) == {"id", "username", "age"}


@pytest.mark.asyncio
class TestGetUserAsync:
    async def test_get_existing_user_200(self, ac: AsyncClient):
        username = fake.user_name()
        age = fake.random_int(min=18, max=80)
        create_resp = await ac.post("/users", json={"username": username, "age": age})
        user_id = create_resp.json()["id"]

        resp = await ac.get(f"/users/{user_id}")
        assert resp.status_code == 200
        assert resp.json()["username"] == username

    async def test_get_nonexistent_user_404(self, ac: AsyncClient):
        resp = await ac.get("/users/99999")
        assert resp.status_code == 404
        assert resp.json()["detail"] == "User not found"


@pytest.mark.asyncio
class TestDeleteUserAsync:
    async def test_delete_existing_user_204(self, ac: AsyncClient):
        create_resp = await ac.post(
            "/users",
            json={"username": fake.user_name(), "age": fake.random_int(min=18, max=80)},
        )
        user_id = create_resp.json()["id"]

        resp = await ac.delete(f"/users/{user_id}")
        assert resp.status_code == 204

    async def test_double_delete_404(self, ac: AsyncClient):
        create_resp = await ac.post(
            "/users",
            json={"username": fake.user_name(), "age": fake.random_int(min=18, max=80)},
        )
        user_id = create_resp.json()["id"]

        resp1 = await ac.delete(f"/users/{user_id}")
        assert resp1.status_code == 204

        resp2 = await ac.delete(f"/users/{user_id}")
        assert resp2.status_code == 404
        assert resp2.json()["detail"] == "User not found"
