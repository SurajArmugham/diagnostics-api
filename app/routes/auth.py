from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.auth_service import create_access_token, verify_credentials
from app.utils.logger import logger


router = APIRouter()


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Exchange credentials for a short-lived JWT.

    Accepts OAuth2 password form data
    (application/x-www-form-urlencoded):
    username=<API_USERNAME>&password=<API_PASSWORD>

    Returns:
        access_token - signed JWT (30 minute expiry).
        token_type   - always "bearer".
    """

    if not verify_credentials(form_data.username, form_data.password):

        logger.warning("Failed login attempt")

        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    logger.info(f"Token issued for {form_data.username}")

    return {
        "access_token": create_access_token(form_data.username),
        "token_type": "bearer"
    }
