from fastapi import APIRouter
from app.models.diagnostics_request import DiagnosticsRequest
from app.services.diagnostics_service import run_diagnostics
from app.services.db_service import get_audit_history
from app.utils.logger import logger


router = APIRouter()


@router.post("/diagnostics")
def diagnostics(request: DiagnosticsRequest):

    logger.info(
        f"Diagnostics Check requested for "
        f"{request.hostname} "
        f"{request.service}"
    )

    result = run_diagnostics(
    request.hostname,
    request.service
)

    return result

@router.get("/audit-history")
def audit_history():

    records = get_audit_history()

    return [
        {
            "id": row[0],
            "hostname": row[1],
            "service": row[2],
            "service_status": row[3],
            "created_at": row[4]
        }
        for row in records
    ]