from fastapi.testclient import TestClient
from unittest.mock import patch

from run import app


client = TestClient(app)


@patch("app.routes.diagnostics.run_diagnostics")
def test_diagnostics(mock_run_diagnostics, auth_headers):

    mock_run_diagnostics.return_value = {
        "hostname": "ProBook.local",
        "disk": "Disk OK",
        "memory": "Memory OK",
        "service": "RUNNING"
    }

    response = client.post(
        "/diagnostics",
        json={
            "hostname": "Localhost",
            "service": "sshd"
        },
        headers=auth_headers
    )

    assert response.status_code == 200

    assert response.json()["service"] == "RUNNING"