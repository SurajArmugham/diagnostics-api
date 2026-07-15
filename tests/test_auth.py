import os

from datetime import datetime, timedelta, timezone

import jwt

from fastapi.testclient import TestClient

from run import app


client = TestClient(app)


def test_token_success():

    response = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "testpass"
        }
    )

    assert response.status_code == 200

    body = response.json()

    assert "access_token" in body

    assert body["token_type"] == "bearer"


def test_token_wrong_password():

    response = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "wrongpass"
        }
    )

    assert response.status_code == 401


def test_diagnostics_requires_token():

    response = client.post(
        "/diagnostics",
        json={
            "hostname": "Localhost",
            "service": "sshd"
        }
    )

    assert response.status_code == 401


def test_invalid_token_rejected():

    response = client.get(
        "/audit-history",
        headers={
            "Authorization": "Bearer garbage"
        }
    )

    assert response.status_code == 401


def test_expired_token_rejected():

    # Hand-craft a token whose "exp" claim is already in
    # the past - proves expiry is enforced per request.
    expired_token = jwt.encode(
        {
            "sub": "testuser",
            "exp": datetime.now(timezone.utc) - timedelta(minutes=5)
        },
        os.getenv("JWT_SECRET_KEY"),
        algorithm="HS256"
    )

    response = client.get(
        "/audit-history",
        headers={
            "Authorization": f"Bearer {expired_token}"
        }
    )

    assert response.status_code == 401


def test_health_open_without_token():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json()["status"] == "UP"
