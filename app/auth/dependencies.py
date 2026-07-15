import jwt

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.auth.auth_service import decode_access_token
from app.utils.logger import logger


# ------------------------------------------------------------
# OAuth2PasswordBearer:
#
# Extracts the token from the Authorization header
# (Authorization: Bearer <jwt>).
#
# tokenUrl="token" tells Swagger UI (/docs) where its
# "Authorize" button should POST credentials, enabling
# interactive testing of protected endpoints.
# ------------------------------------------------------------

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_token(token: str = Depends(oauth2_scheme)) -> dict:
    """
    FastAPI dependency guarding protected routes.

    Decodes and verifies the bearer token. A single
    except on jwt.InvalidTokenError also covers
    jwt.ExpiredSignatureError (its subclass).

    Raises:
        HTTPException 401 when the token is invalid
        or expired.

    Returns:
        Decoded token claims.
    """

    try:
        return decode_access_token(token)

    except jwt.InvalidTokenError:

        logger.warning("Rejected request with invalid or expired token")

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
