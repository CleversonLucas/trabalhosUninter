from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.database import Base, engine
from app import models
from app.api.routes import auth_routes, produto_routes, pedido_routes, auditoria_routes
from app.core.exceptions.handlers import (
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Raízes do Nordeste",
    description="API para gerenciamento de pedidos, estoque e pagamentos simulados.",
    version="1.0.0"
)

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(auth_routes.router)
app.include_router(produto_routes.router)
app.include_router(pedido_routes.router)
app.include_router(auditoria_routes.router)


@app.get("/")
def home():
    return {
        "message": "API Raízes do Nordeste funcionando",
        "status": "online"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "database": "connected"
    }