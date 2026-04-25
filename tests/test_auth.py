import pytest
from fastapi.testclient import TestClient


def test_register_success(client: TestClient, db_session):
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "securepassword123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_register_duplicate_email(client: TestClient, db_session):
    client.post(
        "/auth/register",
        json={"email": "duplicate@example.com", "password": "password123"}
    )
    response = client.post(
        "/auth/register",
        json={"email": "duplicate@example.com", "password": "password456"}
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_register_invalid_email(client: TestClient, db_session):
    response = client.post(
        "/auth/register",
        json={"email": "not-an-email", "password": "password123"}
    )
    assert response.status_code == 422


def test_login_success(client: TestClient, db_session):
    client.post(
        "/auth/register",
        json={"email": "login@example.com", "password": "password123"}
    )
    response = client.post(
        "/auth/login",
        data={"username": "login@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient, db_session):
    client.post(
        "/auth/register",
        json={"email": "wrongpass@example.com", "password": "correctpassword"}
    )
    response = client.post(
        "/auth/login",
        data={"username": "wrongpass@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401


def test_login_nonexistent_user(client: TestClient, db_session):
    response = client.post(
        "/auth/login",
        data={"username": "nobody@example.com", "password": "password123"}
    )
    assert response.status_code == 401


def test_me_authenticated(client: TestClient, db_session):
    client.post(
        "/auth/register",
        json={"email": "me@example.com", "password": "password123"}
    )
    login_response = client.post(
        "/auth/login",
        data={"username": "me@example.com", "password": "password123"}
    )
    token = login_response.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"


def test_me_unauthenticated(client: TestClient, db_session):
    response = client.get("/auth/me")
    assert response.status_code == 401