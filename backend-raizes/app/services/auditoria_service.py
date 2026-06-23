from sqlalchemy.orm import Session

from app.models.log_auditoria import LogAuditoria
from app.repositories.auditoria_repository import listar_logs_auditoria


def registrar_auditoria(
    db: Session,
    usuario_id: int,
    acao: str,
    entidade: str,
    registro_id: int,
    detalhes: str | None = None
):
    log = LogAuditoria(
        usuario_id=usuario_id,
        acao=acao,
        entidade=entidade,
        registro_id=registro_id,
        detalhes=detalhes
    )

    db.add(log)
    db.flush()

    return log


def consultar_logs_auditoria(db: Session):
    return listar_logs_auditoria(db)