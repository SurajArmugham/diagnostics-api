from pydantic import BaseModel


class DiagnosticsRequest(BaseModel):
    hostname: str
    service: str