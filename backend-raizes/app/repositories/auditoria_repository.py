from sqlalchemy.orm import Session

from app.models.log_auditoria import LogAuditoria


def listar_logs_auditoria(db: Session):
    return (
        db.query(LogAuditoria)
        .order_by(LogAuditoria.id.desc())
        .all()
    )