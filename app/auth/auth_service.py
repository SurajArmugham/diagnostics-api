import os
import secrets

from datetime import datetime, timedelta, timezone

import jwt

from dotenv import load_dotenv


load_dotenv()


# ------------------------------------------------------------
# JWT Configuration
#
# ALGORITHM:
# HS256 - symmetric signing. The same JWT_SECRET_KEY
# signs tokens at /token and verifies them on every
# protected request. All replicas share the key via
# the diagnostics-secret Kubernetes Secret, so token
# validation is stateless across pods.
#
# ACCESS_TOKEN_EXPIRE_MINUTES:
# The expiry is stamped INTO the token as the "exp"
# claim at issue time. No server-side timer exists -
# expiry is checked by jwt.decode() on each request.
# ------------------------------------------------------------

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_credentials(username: str, password: str) -> bool:
    """
    Compare submitted credentials against the expected
    API_USERNAME and API_PASSWORD environment variables.

    secrets.compare_digest performs a constant-time
    comparison to prevent timing attacks. Both fields
    are always compared (no short-circuit) so response
    time does not reveal whether the username matched.

    Returns:
        True when both username and password match.
    """

    username_ok = secrets.compare_digest(
        username,
        os.getenv("API_USERNAME", "")
    )

    password_ok = secrets.compare_digest(
        password,
        os.getenv("API_PASSWORD", "")
    )

    return username_ok and password_ok


def create_access_token(subject: str) -> str:
    """
    Issue a signed JWT for the authenticated subject.

    Claims:
        sub - the authenticated username.
        exp - absolute expiry timestamp (UTC).

    Returns:
        Encoded JWT string.
    """

    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": subject,
        "exp": expires_at
    }

    return jwt.encode(
        payload,
        os.getenv("JWT_SECRET_KEY"),
        algorithm=ALGORITHM
    )


def decode_access_token(token: str) -> dict:
    """
    Verify a JWT signature and expiry.

    Raises:
        jwt.InvalidTokenError - bad signature, malformed
        token, or expired "exp" claim
        (jwt.ExpiredSignatureError is a subclass).

    Returns:
        Decoded claims as a dict.
    """

    return jwt.decode(
        token,
        os.getenv("JWT_SECRET_KEY"),
        algorithms=[ALGORITHM]
    )
