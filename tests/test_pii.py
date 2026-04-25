import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


@pytest.fixture
def auth_headers(client: TestClient, db_session: Session) -> dict:
    client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123"}
    )
    response = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "password123"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_scan_requires_auth(client: TestClient, db_session: Session):
    response = client.post(
        "/pii/scan",
        json={"first_name": "John", "last_name": "Doe"}
    )
    assert response.status_code == 401


def test_scan_success(client: TestClient, db_session: Session, auth_headers: dict):
    response = client.post(
        "/pii/scan",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com"
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert data["email"] == "john@example.com"
    assert "id" in data


def test_scan_invalid_name(client: TestClient, db_session: Session, auth_headers: dict):
    response = client.post(
        "/pii/scan",
        json={"first_name": "John123", "last_name": "Doe"},
        headers=auth_headers
    )
    assert response.status_code == 422


def test_scan_phone_validation(client: TestClient, db_session: Session, auth_headers: dict):
    response = client.post(
        "/pii/scan",
        json={"first_name": "John", "last_name": "Doe", "phone": "555-123-4567"},
        headers=auth_headers
    )
    assert response.status_code == 201


def test_list_searches(client: TestClient, db_session: Session, auth_headers: dict):
    client.post(
        "/pii/scan",
        json={"first_name": "Jane", "last_name": "Smith"},
        headers=auth_headers
    )
    response = client.get("/pii/searches", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["first_name"] == "Jane"


def test_get_search_result(client: TestClient, db_session: Session, auth_headers: dict):
    create_response = client.post(
        "/pii/scan",
        json={"first_name": "Bob", "last_name": "Jones"},
        headers=auth_headers
    )
    search_id = create_response.json()["id"]

    response = client.get(f"/pii/searches/{search_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["first_name"] == "Bob"


def test_get_search_result_not_found(client: TestClient, db_session: Session, auth_headers: dict):
    response = client.get("/pii/searches/99999", headers=auth_headers)
    assert response.status_code == 404