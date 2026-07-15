

from unittest.mock import patch

from fastapi.testclient import TestClient

from run import app


client = TestClient(app)


@patch(
    "app.routes.diagnostics.get_audit_history"
)
def test_audit_history(
    mock_get_audit_history,
    auth_headers
):

    mock_get_audit_history.return_value = [
        (
            1,
            "Localhost",
            "sshd",
            "RUNNING",
            "2026-06-12 10:00:00"
        )
    ]

    response = client.get(
        "/audit-history",
        headers=auth_headers
    )

    assert response.status_code == 200

    assert response.json()[0]["hostname"] == "Localhost"

    assert response.json()[0]["service"] == "sshd"

    assert response.json()[0]["service_status"] == "RUNNING"