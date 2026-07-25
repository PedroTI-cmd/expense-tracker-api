from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import DomainError

app = FastAPI(title=settings.app_name)

app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.exception_handler(DomainError)
def domain_error_handler(request: Request, exc: DomainError):
    """Fallback para erros de domínio não tratados explicitamente numa rota."""
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}
