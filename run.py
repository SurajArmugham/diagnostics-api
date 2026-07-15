from contextlib import asynccontextmanager

from fastapi import FastAPI

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