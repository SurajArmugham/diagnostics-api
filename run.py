from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.routes.health import router as health_router
from app.routes.auth import router as auth_router
from app.routes.diagnostics import router as diagnostics_router
from app.services.db_service import create_audit_table


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown lifecycle.
    """

    create_audit_table()

    yield


app = FastAPI(
    title="Incident Diagnostics API",
    lifespan=lifespan
)

app.include_router(health_router)

app.include_router(auth_router)

app.include_router(diagnostics_router)


# ------------------------------------------------------------
# Prometheus Instrumentation
#
# instrument(app):
# Middleware that records, for EVERY request, the
# RED metrics - Rate, Errors, Duration:
#   http_requests_total{handler, method, status}
#   http_request_duration_seconds (histogram)
#
# expose(app):
# Mounts GET /metrics serving the Prometheus text
# format. OPEN by design (industry standard - like
# /health for probes): Prometheus PULLS from inside
# the cluster; production restricts access by
# NETWORK (NetworkPolicy), not by application auth.
#
# include_in_schema=False keeps /metrics out of the
# Swagger UI - it is for machines, not operators.
# ------------------------------------------------------------
Instrumentator().instrument(app).expose(
    app,
    endpoint="/metrics",
    include_in_schema=False
)