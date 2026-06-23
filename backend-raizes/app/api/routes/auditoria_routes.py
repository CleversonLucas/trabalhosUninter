from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.dependencies import exigir_perfis
from app.schemas.auditoria_schema import AuditoriaResponse
from app.services.auditoria_service import consultar_logs_auditoria

router = APIRouter(
    prefix="/auditoria",
    tags=["Auditoria"]
)


@router.get("", response_model=List[AuditoriaResponse])
def listar(
    db: Session = Depends(get_db),
    usuario=Depends(exigir_perfis(["GERENTE", "ADMIN"]))
):
    return consultar_logs_auditoria(db)