import os

import pytest

from fastapi.testclient import TestClient


# ------------------------------------------------------------
# Test-only credentials.
#
# Set BEFORE any test module imports the app so auth code
# (which reads env at call time) sees deterministic values.
#
# These are dummy values for pytest only - real credentials
# live in Infisical and are never needed by the test suite,
# so CI requires no extra GitHub secrets.
#
# Explicit assignment (not setdefault) wins over any local
# .env because load_dotenv() never overrides existing env.
# ------------------------------------------------------------

os.environ["API_USERNAME"] = "testuser"
os.environ["API_PASSWORD"] = "testpass"
os.environ["JWT_SECRET_KEY"] = "test-secret-key-for-pytest-only"


from run import app  # noqa: E402


@pytest.fixture
def auth_headers():
    """
    Obtain a valid JWT from /token using the dummy test
    credentials and return the Authorization header dict.
    """

    client = TestClient(app)

    response = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "testpass"
        }
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }
