from datetime import datetime, timezone

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


def erro_padrao(
    error: str,
    message: str,
    status_code: int,
    path: str,
    details: list | None = None
):
    return JSONResponse(
        status_code=status_code,
        content={
            "error": error,
            "message": message,
            "details": details or [],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "path": path
        }
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    detail = exc.detail

    if isinstance(detail, dict):
        return erro_padrao(
            error=detail.get("error", "ERRO_HTTP"),
            message=detail.get("message", "Erro na requisição."),
            details=detail.get("details", []),
            status_code=exc.status_code,
            path=request.url.path
        )

    return erro_padrao(
        error="ERRO_HTTP",
        message=str(detail),
        details=[],
        status_code=exc.status_code,
        path=request.url.path
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    detalhes = []

    for erro in exc.errors():
        campo = ".".join(str(item) for item in erro.get("loc", []))
        detalhes.append({
            "field": campo,
            "issue": erro.get("msg", "Erro de validação.")
        })

    return erro_padrao(
        error="ERRO_VALIDACAO",
        message="Existem campos inválidos ou obrigatórios não informados.",
        details=detalhes,
        status_code=422,
        path=request.url.path
    )


async def generic_exception_handler(request: Request, exc: Exception):
    return erro_padrao(
        error="ERRO_INTERNO",
        message="Ocorreu um erro interno no servidor.",
        details=[],
        status_code=500,
        path=request.url.path
    )