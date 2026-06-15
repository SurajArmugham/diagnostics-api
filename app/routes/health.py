from fastapi import APIRouter

from app.utils.logger import logger

router = APIRouter()

@router.get("/health")
def health():

    logger.info("Health endpoint called")

    return {
        "status": "UP"
    }